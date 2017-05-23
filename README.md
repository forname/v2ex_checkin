
v2ex 定时自动签到脚本
====================
### 功能
* 每24小时执行一次， 
* 如果v2ex 登录策略更改，程序将会发邮件提醒用户更改代码
* 每次登录成功后信息会放入v2ex.log里面
### 用法
 1. pip install -r requirements.txt
 2. 在 config.py 设置v2ex 用户名密码，以及邮件配置信息
 3. python v2ex.py
linux 下可以用 `nohup python v2ex.py &` 放入后台