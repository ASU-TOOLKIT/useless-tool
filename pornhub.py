# for input ex: https://www.pornhub.com/view_video.php?viewkey=ph5c1926ff70008
# 1.1.1.1 https://play.google.com/store/apps/details?id=com.cloudflare.onedotonedotonedotone
# Copyright by https://instagram.com/reyy05_?igshid=19p0d4zfr5yky 

import requests,re,os,sys,re,json,subprocess,bs4

inp=None

# sys version
def _input_url(string):
	if sys.version_info.major>2:return input(str(string))
	else:return raw_input(string)

# download		
class download:
	def __init__(self):
		pass
		
	@staticmethod
	def get_download_list(url=None):
		try:
			_req = requests.get(url, 
				headers =
					{
						"User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X)"
					}
			)
			if _req.status_code == 200:
				_json = json.loads(
					list(re.findall('var qualityItems_([0-9])*\s\S\s(.*?);',_req.text).pop()).pop()
				);return {"result":_json, "message":"success"}
			else:return {"result":[],"message":"error","error_message":"bad url"}
		except Exception as _e:return {"message":"error","error_message":"%s"%_e}
	
	@staticmethod
	def _input_url_to_download(json=None,show=True):
		global inp
		_list=[]
		_count=0
		_banner="\n\t[ select quality ]\n{}"
		for i in json:
			if i["url"]=="":continue
			_count+=1
			_list.append("\n  %s. QUALITY %s"%(_count,i["text"]))
		
		if show==True:
			print(_banner.format("".join(_list)))
			print("  %s. input url again\n"%str(_count+1))
		while True:
			try:
				c = _input_url("select> ")
				if c==str(_count+1):
					start()
			except Exception as e:
				print("*: error: %s"%e)
			download().ask_before_download(url=json[int(c)-1]["url"], json=json)

			
	@staticmethod
	def _tanya(output=None):
		print("*: SAVED AS: %s"%output)
		g=_input_url("?: view (y/n) > ")
		if g=="y":
			subprocess.Popen(["am","start","file://"+output]).wait()
			print("\n* finisned.");start()
		else:print("\n*: finished.");_input_url("press enter to again...");start()
	
	@staticmethod
	def ask_before_download(url=None, json=None):
		global inp
		c = _input_url("?: [S]ee video or [D]ownload or [B]ack? [S/D/B]> ").lower()
		if c=="d":
			subprocess.Popen([
				"curl","-o",
					inp.split("/").pop().replace("view_video.php?viewkey=","")+".mp4",url]).wait()
			f=os.getcwd()+"/"+inp.split("/").pop().replace("view_video.php?viewkey=","")+".mp4"
			download()._tanya(output=f)
		elif c=="b":
			download()._input_url_to_download(json=json)
		else:
			subprocess.Popen(["am","start",url],
				stdout=subprocess.PIPE,
					 stdin=subprocess.PIPE,stderr=subprocess.PIPE).wait()
			download().ask_before_download(url=url, json=json)

def xnxx(url=None):
	try:
		result=[]
		b=bs4.BeautifulSoup(
			requests.get(url).text,"html.parser")
		for i in b.find_all("a",href=True):
			if "mp4" in i["href"]:
				if "qual" in i.text.lower():
					result.append(
						{
							"url":i["href"],
							"text":i.text.lower().replace("view","").replace(" qual","")
						}
					)
		if len(result) !=0:
			return {"message":"success","result":result}
		else:
			return {"message":"error"}
	except Exception as e:
		return {"message":"error: %s"%e}

def mulai(type=None):
	global inp
	inp=_input_url('?: video url: ') 
	if inp=="":mulai(type=type)
	elif inp=="back":start()
	else:
		if type=="pornhub":
			json=download().get_download_list(url=inp)
			if json["message"]=="error":
				print("*: error: %s"%json["error_message"]);mulai(type=type)
			else:
				download()._input_url_to_download(
					json=download().get_download_list(url=inp)["result"])
		elif type=="xnxx":
			json=xnxx(url=inp)
			if "error" in json["message"]:
				print("*: error: %s"%json["message"]);mulai(type=type)
			else:
				download()._input_url_to_download(json=json["result"])
	
def start():
	global inp
	os.system("clear")
	print("\t\t[ bokep downloader ]\n\n* use 1.1.1.1 apk to use this tool\n* https://play.google.com/store/apps/details?id=com.cloudflare.onedotonedotonedotone\n\n")
	print("  1. pornhub\n  2. xnxx\n  3. xvideos\n")
	while True:
		inp=_input_url("?: menu: ")
		if inp=="":continue
		elif inp in ["1","01"]:
			print("*: press 'back' to back.")
			mulai(type="pornhub")
		elif inp in ["2","02"]:
			print("*: press 'back' to back.")
			mulai(type="xnxx")
		elif inp in ["3","03"]:
			print("*: press 'back' to back.")
			mulai(type="xnxx")
		else:print("*: wrong input.")

if __name__=="__main__":
	start()
