#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# Copyright (C) 2023 , Inc. All Rights Reserved 
# @Time    : 2023/5/17 22:45
# @Author  : raindrop
# @Email   : 1580925557@qq.com
# @File    : main.py

from requests import get, head
from json import loads, load
from re import findall
from os import mkdir, path
from time import sleep, localtime, strftime, time
import re
import csv
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from fmt import debug, info


class Task(object):

    def __init__(self, sec_user_id, download_num, thread_num, cookie):
        self.sec_user_id = sec_user_id
        # 记录需要下载的作品个数
        self.count = download_num
        # 记录开启得的线程数量
        self.tc = thread_num
        self.cookie = cookie

        self.max_cursor = int(round(time() * 1000))
        self.picture = 0
        self.video = 0
        self.numb = 0
        self.nickname = "Null"
        self.time_start = float(round(time()))
        self.base_path = "./download"

    def run(self):
        url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=' + self.sec_user_id + '&max_cursor=' + str(
            self.max_cursor) + '&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'

        headers = {
            'referer': 'https://www.douyin.com/user/' + self.sec_user_id,
            'cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36'
        }

        resp = get(url, headers=headers)
        resp = resp.text.encode('utf-8').decode('utf-8')
        try:
            debug(url)
            resp = loads(resp)
        except:
            info(
                'cookies失效，请自行获取cookies填入脚本目录下cookie.txt中\n获取cookies方法：\n1.电脑浏览器打开抖音并登录,随便找一个人的主页打开\n2.按f12键进入开发者模式，点击网络\n3.刷新页面,网络的名称里选择第一个\n4.标头，下滑找到cookie，右键复制值')
            a = input("请输入新的cookies：")
            with open('cookie.txt', 'w+') as f:
                f.write(a)
            input('回车退出')
            exit()

        # 定义存储数据的路径
        folder_path = self.base_path

        if self.numb == 0:
            try:
                self.nickname = resp["aweme_list"][0]["author"]["nickname"]
                folder_path += '/' + self.nickname

                info('即将 {} 线程采集 {} 个 {} 的作品'.format(str(self.tc), str(self.count), self.nickname))
                # input('回车继续')
                time_start = float(round(time()))
                mkdir(folder_path + "/")
                mkdir(folder_path + "/video/")
                mkdir(folder_path + "/picture/")
                info("首次创建{}缓存文件夹".format(self.nickname))
            except:
                info("{}缓存文件夹已存在".format(self.nickname))
                return

            # 创建记录的信息
            with open(folder_path + "/" + self.nickname + "_采集数据.csv", 'w', newline='', encoding='utf-8',
                      errors='ignore') as csvfile:
                fieldnames = ['aweme_id', '时间', 'title', '格式', '收藏', '评论', '点赞', '分享', 'share_url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        info('共{}个作品，已保存{}个，当前解析到{}'.format(str(self.count), str(self.numb), len(resp["aweme_list"])))

        # 根据需求截取信息
        if self.count == '∞':
            aweme_list = resp["aweme_list"]
        elif len(resp["aweme_list"]) > (int(self.count) - int(self.numb)):
            aweme_list = resp["aweme_list"][:(int(self.count) - int(self.numb))]
        else:
            aweme_list = resp["aweme_list"]

        pool = ThreadPoolExecutor(self.tc)

        for aweme in aweme_list:
            pool.submit(self.download, folder_path, aweme)
            self.numb = self.numb + 1
        pool.shutdown()

        if str(self.numb) == str(self.count):
            info("已采集指定数目作品,共{}个作品,{}个视频，{}个图片，请在脚本目录下查看".format(self.numb, self.video, self.picture))
            self.time_cha()
        if resp["has_more"] == 0:
            info("数据采集结束,共{}个作品,{}个视频，{}个图片，请在脚本目录下查看".format(self.numb, self.video, self.picture))
            self.time_cha()
        self.max_cursor = resp["max_cursor"]

    def time_cha(self):
        info('运行结束')
        time_end = float(round(time()))
        time_diff = int(time_end - self.time_start)
        if time_diff >= 3600:
            hh = time_diff // 3600
            time_diff = time_diff % 3600
        else:
            hh = 0
        if time_diff >= 60:
            mm = time_diff // 60
            time_diff = time_diff % 60
        else:
            mm = 0
        if time_diff > 0:
            ss = time_diff
        info('本次执行共耗时{}时{}分{}秒'.format(str(hh), str(mm), str(ss)))

    def download(self, folder_path: str, aweme):
        try:
            desc = aweme["statistics"]
            desc['收藏'] = desc.pop('collect_count')
            desc['评论'] = desc.pop('comment_count')
            desc['点赞'] = desc.pop('digg_count')
            desc['分享'] = desc.pop('share_count')
            # 修复bug
            desc['share_url'] = aweme['share_info']['share_url']
        except Exception as e:
            print("[debug] Exception: ", repr(e))
        if aweme['images'] is None:
            desc['格式'] = "video"
        else:
            desc['格式'] = "picture"
        del desc['play_count']
        del desc['admire_count']
        time_1 = int(aweme["create_time"])
        # 转换成localtime
        time_2 = localtime(time_1)
        # 转换成新的时间格式
        desc['时间'] = strftime("%Y-%m-%d %H:%M:%S", time_2)
        desc['title'] = aweme['desc']
        with open(folder_path + "/" + self.nickname + "_采集数据.csv", 'a', newline='', encoding='utf-8',
                  errors='ignore') as csvfile:
            fieldnames = ['aweme_id', '时间', 'title', '格式', '收藏', '评论', '点赞', '分享', 'share_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(desc)

        # 视频
        if aweme['images'] is None:
            url = aweme["video"]["play_addr"]["url_list"][0]
            try:
                video = get(url)
                # 添加基础路径
                download_path = folder_path + "/video/"
                with open(download_path + aweme["aweme_id"] + '.mp4', 'wb') as f:
                    f.write(video.content)
                self.video += 1
            except Exception as e:
                debug(repr(e))
        else:
            url_list = aweme["images"]
            s = 0
            for i in url_list:
                s += 1
                url = i["url_list"][0]
                video = get(url)
                with open(aweme["author"]["nickname"] + "/picture/" + aweme["aweme_id"] + '_' + str(s) + '.jpeg',
                          'wb') as f:
                    f.write(video.content)
                self.picture += 1


def now():
    time_1 = int(time())
    # 转换成localtime
    time_2 = localtime(time_1)
    # 转换成新的时间格式
    nows = strftime("%Y-%m-%d %H:%M:%S", time_2)
    return nows


# 读取url列表
def read_url_list(file_path: str) -> list[str]:
    url_list = []

    # 打开存储URL地址的文件 并读取
    with open(file_path) as f:
        read_data = f.readlines(-1)
        for url in read_data:
            if re.match("https://www.douyin.com/user/*", url):
                url_list.append(url.strip())

        f.close()

    return url_list


def read_config_info(file_path: str) -> dict:
    with open(file_path) as f:
        config_info = load(f)
        f.close()
        return config_info


def main():
    debug(now())
    info("github开源地址:https://github.com/raindrop-hb/douyin_spider\n使用请保留版权\n欢迎使用raindrop抖音爬虫_解析工具")

    # 读取配置信息
    config_info = read_config_info("./config.json")

    # 读取URL地址
    user_urls = read_url_list(config_info["urls_path"])
    if len(user_urls) <= 0:
        info("无链接")

    thread_num = config_info["thread_num"]
    download_num = config_info["download_num"]
    cookie = read_cookie(config_info["cookie_path"])

    for url in user_urls:
        a = 'https' + findall('https(.*)', url)[0]
        # a = head(a)
        # headers={
        #     "cookie":cookie()
        # }
        # a = str(a.headers.get('location'))
        # a = head(a,headers=headers).headers['Location']
        a = a.replace('https://www.douyin.com/user/', '').replace('?previous_page=web_code_link', '').replace(
            '?previous_page=app_code_link', '')
        task = Task(a, download_num, thread_num, cookie)
        task.run()


def read_cookie(cookie_path: str):
    with open(cookie_path, 'r') as f:
        c = f.read()
    return str(c)


if __name__ == '__main__':
    main()
