from PIL import Image, ImageDraw, ImageFont
import logging
import requests
import xml.etree.ElementTree as ET
import random
from io import BytesIO
from bs4 import BeautifulSoup
from colorsys import rgb_to_hsv, hsv_to_rgb
import wikiquote
import re
import time

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

def MakeAlbum(BandName, loc, timestamp):
	try:
		imageWidth, imageHeight = (500,500)
		fontSize = 50

		AlbumArt = Image.open("image.jpg", "r").convert('RGBA')
		AlbumArt = AlbumArt.resize((500,500))
		r, g, b, t = AlbumArt.getpixel((1, 1))
		if ((250 - r) < 125):
			r, g, b = 33, 21, 29
		elif ((250 - r) > 125):
			r, g, b = 255, 255, 255

		bandText = Image.new('RGBA', AlbumArt.size, (r,g,b,0))
		bandFont = ImageFont.truetype('Besom.ttf', fontSize)
		draw = ImageDraw.Draw(bandText)
		textWidth, textHeight = draw.textsize(str(BandName), font=bandFont)
		while (textWidth > imageWidth):
			fontSize -= 10
			bandFont = ImageFont.truetype('Besom.ttf', fontSize)
			draw = ImageDraw.Draw(bandText)
			textWidth, textHeight = draw.textsize(str(BandName), font=bandFont)

		draw.text((10,60), BandName, font=bandFont, fill=(r,g,b,255))
		AlbumArt = Image.alpha_composite(AlbumArt, bandText)

		r, g, b, t = AlbumArt.getpixel((1, 499))
		if ((250 - r) < 125):
			r, g, b = 33, 21, 29
		elif ((250 - r) > 125):
			r, g, b = 255, 255, 255

		songText = Image.new('RGBA', AlbumArt.size, (r,g,b,0))
		songFont = ImageFont.truetype('Cabana.otf', 40)
		draw = ImageDraw.Draw(songText)
		textWidth, textHeight = draw.textsize(GetSongTitle(), font=songFont)
		draw.text(((imageWidth - textWidth)/2, 400), GetSongTitle(), font=songFont, fill=(r,g,b,255))
		AlbumArt = Image.alpha_composite(AlbumArt, songText)

		AlbumArt.save(loc + "album_" + str(timestamp) + ".png")
	except:
		MakeAlbum(GetBandName())

def GetSongTitle():
	try:
		page = wikiquote.random_titles(max_titles=1)
		quote = wikiquote.quotes(page[0], max_quotes=1)[0]
		quote = re.split('; |, |\? |\. |\! |: ', quote)
		quote = quote[0]
		quoteLength = len([i for i in quote.split()])
		if (quoteLength > 7):
			quote = quote.split(' ')[:5]
			quote = ' '.join(quote)

		return quote
	except:
		time.sleep(1)
		GetSongTitle()
	

def FakeAlbum(loc=""):
	timestamp = str(int(time.time()))
	DownloadImage(RandImage())
	MakeAlbum(GetBandName(), loc, str(timestamp))

	imageName = "album_" + str(timestamp) + ".png"

	return imageName