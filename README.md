# 抖音爬虫

<p align="center">
    <a href="https://github.com/raindrop-hb"><img alt="Author" src="https://img.shields.io/badge/author-raindrop-blueviolet"/></a>
    <img alt="PHP" src="https://img.shields.io/badge/code-Python-success"/></a>
    <a href="https://jq.qq.com/?_wv=1027&k=fzhZMSbP"><img alt="QQ群" src="https://img.shields.io/badge/QQ-交流群-blackviolet"/></a>
</p>

通过抖音官方接口，爬取用户所有视频和图片并创建excel数据

原项目地址: https://github.com/raindrop-hb/douyin_spider

------
目前已实现功能：


- [x] 自动爬取
- [x] 检测cookie
- [x] 整理数据

如有其他好的建议请提交issues

## 环境要求
python 3.6 

## 使用方法	
1. 使用浏览器登陆[任意抖音主页](https://www.douyin.com/user/MS4wLjABAAAAReXxwTVnBAfcJ6-JIQRd4ZrCjxqrWi-cnT8kvK5zinc)，然后按下`ctrl+shift+i`进入开发者模式，选择网络，并点击第1个请求，复制`Set-Cookie`字段内容

   ![screenshot1](img/screenshot1.png)

2. 将上述字段内容替换根目录中`cookie.txt`文件的内容
3. 运行输入`python main.py`函数，根据提示一次输入对应信息

# donate

如果该项目对您有帮助，欢迎捐赠

<table>
  <tr>
    <th width="33.3%">支付宝</th>
    <th width="33.3%">微信</th>
    <th width="33.3%">QQ群</th>
  </tr>
  <tr></tr>
  <tr align="center">
    <td><img width="70%" src="https://github-production-user-asset-6210df.s3.amazonaws.com/72308008/249005291-da996bc0-37fe-4ac7-b29b-357af69d4c28.png"></td>
    <td><img width="70%" src="https://github-production-user-asset-6210df.s3.amazonaws.com/72308008/249005176-6327e7d8-b69e-4100-b3d7-ee27403dabf6.png"></td>
    <td><img width="70%" src="https://github-production-user-asset-6210df.s3.amazonaws.com/72308008/249005430-6a9ad701-b9fa-4c88-98d4-2cbb01f7829b.png"></td>
  </tr>
</table>
