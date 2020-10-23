# ----- import -----
# local
from core.utils import check, date, load_settings, write_msg
from core.plugin import PluginManager

# global
import sys
import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from colorama import Fore, Back, Style
import colorama
colorama.init()
# -----

name = f'{Fore.MAGENTA}<{Fore.RED}sirai{Fore.MAGENTA}>{Fore.RESET}'

class Sirai(object):
	"""docstring for Sirai"""
	def __init__(self, load=False):
		
	# load
		if load:
			settings = load_settings()
			print(f'{date()} {name} {Fore.YELLOW}connecting to VK LongPoll...{Fore.RESET}')
			self.vk = vk_api.VkApi(token=settings['token'])
			self.longpoll = VkBotLongPoll(self.vk, settings['group_id'])
		else:
			print(f'{date()} {name} {Fore.RED}the connection is canceled, press "load" set to "True"{Fore.RESET}')

# check settings
	settings = load_settings()
	pluginsys = PluginManager()
	
# print settings
	def banner(self):
		print(f' _______ _________ _______  _______ _________   ______   _______ _________')
		print(f'(  ____ \\__   __/(  ____ )(  ___  )\\__   __/  (  ___ \\ (  ___  )\\__   __/')
		print(f'{Fore.MAGENTA}| (    \\/   ) (   | (    )|| (   ) |   ) (     | (   ) )| (   ) |   ) (   {Fore.RESET}')
		print(f'{Fore.BLUE}| (_____    | |   | (____)|| (___) |   | |     | (__/ / | |   | |   | |   {Fore.RESET}')
		print(f'{Fore.CYAN}(_____  )   | |   |     __)|  ___  |   | |     |  __ (  | |   | |   | |   {Fore.RESET}')
		print(f'{Fore.GREEN}      ) |   | |   | (\\ (   | (   ) |   | |     | (  \\ \\ | |   | |   | |   {Fore.RESET}')
		print(f'{Fore.YELLOW}/\\____) |___) (___| ) \\ \\__| )   ( |___) (___  | )___) )| (___) |   | |   {Fore.RESET}')
		print(f'{Fore.RED}\\_______)\\_______/|/   \\__/|/     \\|\\_______/  |/ \\___/ (_______)   )_(   {Fore.RESET}')
		print('===========================================================================')
		print(f'by: {Fore.MAGENTA}salormoon_project{Fore.RESET}, {Fore.GREEN}simple bot for VK with automatic plug-ins{Fore.RESET}')
		print('===========================================================================')

	def print_settings(self):
		settings = load_settings()
		print(f'----- < {Fore.CYAN}settings{Fore.RESET} > -----')
		for x in settings:
			arg = settings[x]
			print(f'{x}: {Fore.GREEN}{arg}{Fore.RESET}')
		print(f'{Fore.GREEN}----- {Fore.RESET}< {Fore.CYAN}settings{Fore.RESET} > {Fore.GREEN}-----{Fore.RESET}')

# load plugins
	def load(self, plugin_dir):
		print(f'{date()} {name} {Fore.YELLOW}load plugins...{Fore.RESET}')
		check('folder', plugin_dir)
		settings = load_settings()
		self.pluginsys.Load(plugin_dir, settings)
		print(f'{date()} {name} {Fore.GREEN}load complete!{Fore.RESET}')

	# ----- long polling -----
	def run(self, admins = False):
		settings = load_settings()
		print(f'{Fore.MAGENTA}start longpooling...{Fore.RESET}')
		for event in self.longpoll.listen():
			
			if event.type == VkBotEventType.MESSAGE_NEW:
				data = event.object.message
				peer_id = data['peer_id']
				from_id = data['from_id']
				try:
					text = data['text']
				except Exception as e:
					text = None
				try:
					reply = data['reply_message']
					reply_id = reply['from_id']
				except Exception as e:
					pass

				text = text.split(' ',1)
				cmd = text[0]
				try:
					args = text[1]
				except Exception as e:
					args = None
				print(f'{date()} <{Fore.MAGENTA}{from_id}{Fore.RESET}> event text: {Fore.YELLOW}{cmd} {Fore.MAGENTA}{args}{Fore.RESET}', end=' |')

		# ----- обработчик комманд -----
				self.pluginsys.answer(data, cmd, args, admins)

				if from_id == settings['main_admin'] and cmd== '/off':
					write_msg(data, 'выключаюсь, мой господин')
					print(f'{Fore.RED}[admin] bot off...{Fore.RESET}')
					sys.exit()