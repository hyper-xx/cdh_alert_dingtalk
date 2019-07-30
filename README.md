# cdh_alert_dingtalk
Monitor cdh with dingtalk alert.

##简介
监听cdh故障事件，并发送告警信息到钉钉

##使用方法
配置config.conf文件，指定需要监控的cdh api url，并填写cdh用户。配置钉钉机器人token🤖，使用crontab启动即可。

```
config.conf

[cm]  //配置cdh api的url及验证账户密码
cm_host=http://cm.***.com/api/v14/
cm_user=******
cm_passwd=******



[alert] //配置钉钉机器人token及需要单独@提醒人的手机号
dingrobot=https://oapi.dingtalk.com/robot/send?access_token=****************
notice=["12345678910"]
```
