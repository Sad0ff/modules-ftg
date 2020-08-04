from .. import loader, utils
import functools
from telethon import events
import logging
import pytube
logger = logging.getLogger(__name__)


def register(cb):
    cb(DownloadYTMod())
    
class DownloadYTMod(loader.Module):
    """DownloadYT"""
    strings = {
        'name': 'DownloadYT',
        'usage': 'Напиши <code>.help DownloadYT</code>',
    }
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []
    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()
        
    async def dytcmd(self, message):
        """отправляет видеов чат по ссылке из ютуба\n@offsd подпишись-пожалеешь"""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        chatid = str(message.chat_id)
        if not args:
            if not reply:
                await utils.answer(message, self.strings('usage', message))
                return
            else:
                txt = reply.raw_text
        else:
            txt = utils.get_args_raw(message)
        await message.edit("<b>Извиняемся...</b>")
        link =f"\"{txt}\""
        yt = pytube.YouTube(link)
        stream = yt.streams.first()
        await message.client.send_file(message.to_id, stream.download(), reply_to=reply)
        await message.delete()
    