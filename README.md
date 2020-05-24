# Nessus_update

主要是解决某几位大佬为了寻找nessus的all-2.0.tar.gz头疼的问题造就的轮子

```
python get_activ_code.py
```

```
生成的Email地址: g8orwvd0e@getnada.com
开始获取Nessus注册相关的表单
获取到Nessus注册token为	dchn8Fcnky6mLc5dGDDMHRxu0U6ZyenOT6+Ky0d7rUo=
注册成功，等待到邮箱 g8orwvd0e@getnada.com 去获取相关的信息
需要等待一段时间(15秒)，等待邮箱收信有一定的延迟
获取到邮箱 g8orwvd0e@getnada.com 的内容uid: yqu6hlX4b8c5N3fwuqDUxOpTXkcHoA
Nessus 的激活码Activation code: 1E12-AB04-8DDB-564C-F119
获取到nessus插件包的下载地址是: https://plugins.nessus.org/v2/nessus.php?f=all-2.0.tar.gz&u=501b33370d5649f73e029b246eedc3fe&p=1b1ec8c81448c67a986cd397232acb1b
```

some tips

```
service nessusd stop
# curl  https://www.tenable.com/downloads/api/v1/public/pages/nessus/downloads/10204/download?i_agree_to_tenable_license_agreement=true -o nessus880.deb
# dpkg -i nessus880.deb
# mv /opt/nessus/var/nessus/templates/metadata.json /opt/nessus/var/nessus/templates/metadata.json.old1
# mv /opt/nessus/var/nessus/templates/tmp/metadata.json /opt/nessus/var/nessus/templates/tmp/metadata.json.old1

/opt/nessus/sbin/nessuscli update  /root/all-2.0.tar.gz
# just for first update all-2.0.tar.gz
# cp /opt/nessus/var/nessus/www/policy_wizards.json /opt/nessus/var/nessus/www/policy_wizards.json.bak
# sed -i '/subscription_only": true,/d' /opt/nessus/var/nessus/www/policy_wizards.json
# sed -i '/"manager_only": true,/d' /opt/nessus/var/nessus/www/policy_wizards.json
# sed -i 's/"HomeFeed (Non-commercial use only)"/"ProfessionalFeed (Direct)"/g' /opt/nessus/var/nessus/plugin_feed_info.inc
# sed -i 's/"HomeFeed (Non-commercial use only)"/"ProfessionalFeed (Direct)"/g' /opt/nessus/lib/nessus/plugins/plugin_feed_info.inc
# sed -i 's/Nessus Home/Nessus/g' /opt/nessus/lib/nessus/plugins/scan_info.nasl
# cp /opt/nessus/etc/nessus/nessus-fetch.db.bak /opt/nessus/etc/nessus/nessus-fetch.db
service nessusd start
```
