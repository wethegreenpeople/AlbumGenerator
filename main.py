from PIL import Image, ImageDraw, ImageFont
import logging
import requests
import xml.etree.ElementTree as ET
import random
from io import BytesIO
from bs4 import BeautifulSoup

def RandImage():
	payload = {
		'method':'flickr.interestingness.getList',
		'api_key':'',
		'per_page':300
	}
	flickr = requests.get('https://api.flickr.com/services/rest/?', params=payload)
	root = ET.fromstring(flickr.text)

	randomPhoto = random.randint(0,299)
	photoId = root[0][randomPhoto].attrib['id']
	photoFarm = root[0][randomPhoto].attrib['farm']
	photoServer = root[0][randomPhoto].attrib['server']
	photoSecret = root[0][randomPhoto].attrib['secret']
	photoUrl = "https://farm{0}.staticflickr.com/{1}/{2}_{3}_b.jpg".format(photoFarm, photoServer, photoId, photoSecret)

	return photoUrl

def DownloadImage(photoUrl):
	photo = requests.get(photoUrl).content
	Image.open(BytesIO(photo)).save("image.jpg")

def GetBandName():
	try:
		wikiPage = requests.get("https://en.wikipedia.org/wiki/Special:Random")
		soup = BeautifulSoup(wikiPage.content, "html.parser")
		bandName = soup.h1.string
		nameLength = len([i for i in bandName.split()])

		if (nameLength > 4):
			GetBandName()
		else:
			return bandName
	except:
		GetBandName()

def MakeAlbum(BandName):
	AlbumArt = Image.open("image.jpg", "r").convert('RGBA')
	AlbumArt = AlbumArt.resize((500,500))
	txt = Image.new('RGBA', AlbumArt.size, (255,255,255,0))
	fnt = ImageFont.truetype('Besom.ttf', 80)
	d = ImageDraw.Draw(txt)
	d.text((10,60), BandName, font=fnt, fill=(255,255,255,255))
	out = Image.alpha_composite(AlbumArt, txt)
	out.save("album.png")

DownloadImage(RandImage())
MakeAlbum(GetBandName())