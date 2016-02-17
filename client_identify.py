# -*- coding:gb18030 -*-
import sys,re

def identify(id):
	if re.match('.*((baidubrowser)( \\d+)?).*',id) or re.match('.*((BIDUBrowser)( \\d+)?).*',id) or re.match(".*(?=Mozilla/5\.0 \(iPad; (?:U; CPU|CPU (?:iPhone )?OS)).*?(BaiduHD) (\d+)\.(\d+)\.?(\d+)?.*",id) or re.match(".*(BIDUPlayerBrowser)(?:/(\d+)).*",id):
		cl = "Baidu"
	elif re.match('.*(360SE|360EE).*',id):
		cl = "360"
	elif re.match('.*((SE) \\d+)\\.X.*',id):
		cl = "Sogou"
	elif re.match('.*(GreenBrowser).*',id):
		cl = "GreenBrowser"
	elif id.find("Maxthon") >= 0:
		cl = "遨游"
	elif re.match('.*(MyIE2).*',id):
		cl = "MyIE2"
	elif re.match('.*((TencentTraveler)( \\d+)?).*',id):
		cl = "TT"
	elif re.match('.*(2345Explorer).*',id):
		cl = "2345"
	elif re.match('.*(Ruibin).*',id):
		cl = "瑞影"
	elif re.match('.*((TaoBrowser)(\\/\\d+)?).*',id) or re.match('.*((Alibrowser)( \\d+)?).*',id):
		cl = "Alibaba"
	elif id.find("LBBROWSER") >= 0:
		cl ="猎豹"
	elif re.match('.*([^M]|^)((QQBrowser)(\\/\\d+)?).*',id):
		cl = "QQ"
	elif id.find("CoolNovo") >= 0:
		cl = "枫树"
	elif re.match('.*MS((IE) \\d+).*',id):
		cl = "IE"
	elif re.match('.*((Firefox)(\\/\\d+)?).*',id):
		cl = "Firefox"
	elif re.match('.*(?=.*?Opera).*?(Version\\/\\d+)?.*',id):
		cl = "Opera"
	elif re.match('.*((Chrome)(\\/\\d+)?).*',id):
		cl = "Chrome"
	elif re.match('.*(?=.*?Safari).*?(Version\\/\\d+)?.*',id):
		cl = "Safari"
	else:
		cl = "Other"
	return cl
