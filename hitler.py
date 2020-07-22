from telethon import events
from .. import loader, utils
import os
import requests
from PIL import Image,ImageFont,ImageDraw 
import re
import io
from textwrap import wrap

def register(cb):
	cb(HitlerMod())
	
class HitlerMod(loader.Module):
	"""Hitler"""
	strings = {
		'name': 'Hitler',
		'usage': 'Напиши <code>.help Цитатник Гитлера</code>',
	}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
		
	async def hcmd(self, message):
		""".h <реплай на сообщение/свой текст>\n@offsd подпишись-пожалеешь"""
		
		ufr = requests.get("https://github.com/Sad0ff/modules-ftg/raw/master/open-sans.ttf")
		f = ufr.content
		
		reply = await message.get_reply_message()
		args = utils.get_args_raw(message)
		if not args:
			if not reply:
				await utils.answer(message, self.strings('usage', message))
				return
			else:
				txt = reply.raw_text
		else:
			txt = utils.get_args_raw(message)
		await message.edit("<code>Ehre sei Hitler...</code>")
		pic = requests.get("https://raw.githubusercontent.com/Sad0ff/modules-ftg/master/offsd.jpg")
		pic.raw.decode_content = True
		img = Image.open(io.BytesIO(pic.content)).convert("RGB")
 
		W, H = img.size
		text = "\n".join(wrap(txt, 19))
		t = text + "\n"
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
		w, h = draw.multiline_textsize(t, font=font)
		imtext = Image.new("RGBA", (w+10, h+10), (0, 0,0,0))
		draw = ImageDraw.Draw(imtext)
		draw.multiline_text((10, 10),t,(255,255,255),font=font, align='left')
		imtext.thumbnail((339, 166))
		img.paste(imtext, (10,10), imtext)
		out = io.BytesIO()
		out.name = "offsd.jpg"
		img.save(out)
		out.seek(0)
		await message.client.send_file(message.to_id, out, reply_to=reply)
		await message.delete()