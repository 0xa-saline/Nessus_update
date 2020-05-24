#!/usr/bin/python
#coding:utf-8
import warnings
import requests
import string
import random
import time
import json
import re
import sys
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def str_count(count):
	return ''.join(random.choice(string.letters + string.digits) for i in range(count)) 

headers = {
	"Connection": "close", 
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36", 
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
	"Sec-Fetch-Site": "none", 
	"Sec-Fetch-Mode": "navigate",
	"Sec-Fetch-User": "?1",
	"Sec-Fetch-Dest": "document",
	"Accept-Language": "zh-CN,zh;q=0.9,es;q=0.8,fr;q=0.7,vi;q=0.6"
}
# 该代理需要具备一些爬墙的功能
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

mailx = str(str_count(9).lower())
domain = "getnada.com"
name = mailx

email = mailx + '@getnada.com'  
print ("生成的Email地址: {mail}".format(mail=email))
#regurl = "https://www.tenable.com/products/nessus/nessus-essentials?tns_redirect=true"
regurl = "https://zh-cn.tenable.com/products/nessus/nessus-essentials?tns_redirect=true"
print ("开始获取Nessus注册相关的表单")
try:
	ht=requests.get(regurl,headers=headers, verify=False,proxies=proxies,timeout=600)
	bs=BeautifulSoup(ht.text,'html.parser')
	for link in bs.findAll("input",{"name":"token"}):
		if 'name' in link.attrs:
			tkn=link.attrs['value']
		else:
			print("没有在当前页面找到token")
except Exception as e:
	print '[get token] {}'.format(e.message)
	pass
print ("获取到Nessus注册token为\t{token}".format(token=tkn))
comurl = "https://www.tenable.com/products/nessus/nessus-essentials"
params={"first_name":"John","last_name":"Smith","email":email,"country":"IN","Accept":"Agree","robot":"human","type":"homefeed","token":tkn,"submit":"Register"}
try:
	r = requests.post(comurl,headers=headers, data=params, verify=False,proxies=proxies,timeout=600)
except Exception as e:
	print '[reg] {}'.format(e.message)
	pass
all = mailx + "@" + domain
print ("注册成功，等待到邮箱 {mail} 去获取相关的信息".format(mail=all))
GET_INBOX = 'https://getnada.com/api/v1/inboxes/'
boxurl = GET_INBOX + all
sleep = 15
print ("需要等待一段时间({sleep}秒)，等待邮箱收信有一定的延迟".format(sleep=sleep))

time.sleep(sleep)
try:
	r = requests.get(boxurl,headers=headers,proxies=proxies,timeout=600, verify=False)
	uid = (r.json()['msgs'])[0]['uid']
	print("获取到邮箱 {mail} 的内容uid: {uid}".format(mail=all,uid=uid))
except Exception as e:
	print '[get box] {}'.format(e.message)
	pass


GET_MESSAGE = 'https://getnada.com/api/v1/messages/'
activ_code = ''
try:
	r = requests.get(GET_MESSAGE + uid,headers=headers,proxies=proxies,timeout=600, verify=False)
	text = r.json()['html']
	regex = r"\w{4}(?:-\w{4}){4}"
	activation_code=re.search(regex,text)
	activ_code = activation_code.group()
	print("Nessus 的激活码Activation code: {code}".format(code=activation_code.group()))
except Exception as e:
	print '[get message] {}'.format(e.message)
	pass
'''
run in system

import os
if os.name == 'nt':
	os.system( '""C:\\\\Program Files\\\\Tenable\\\\Nessus\\\\nessuscli" fetch --register "' + str(activation_code.group()))
	os.system( '""C:\\\\Program Files\\\\Tenable\\\\Nessus\\\\nessuscli" update "')
else:
	cmd = ('/opt/nessus/sbin/nessuscli fetch --register ' + str(activation_code.group()) + ';/opt/nessus/sbin/nessuscli update; systemctl restart nessusd')
	os.system(cmd)
'''

nessid= "https://52.16.241.207/register.php?serial={active}".format(active=activ_code)
try:
	resp = requests.get(nessid,headers=headers,proxies=proxies,timeout=600, verify=False)
	content = resp.content
	text = content.strip().split('\n')
	allurl = "https://plugins.nessus.org/v2/nessus.php?f=all-2.0.tar.gz&u={u}&p={p}"
	fina = allurl.format(u=text[1],p=text[2])
	print "获取到nessus插件包的下载地址是:",fina
except Exception as e:
	print '[-] {}'.format(e.message)
	pass
