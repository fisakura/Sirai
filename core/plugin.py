import os
import sys
import colorama
from core.utils import check, check_role, load_settings
from colorama import Fore

LoadedPluginsData = []

class Plugin(object):
	def __init__(self, name='', preffix='', usage='', sim='🔷'):
		self.name = name
		self.preffix = preffix
		self.usage = usage
		self.sim = sim
		self.commands = {}
		self.plugin_data = {'commands':self.commands, 'name':self.name,'preffix':self.preffix, 'usage':self.usage, 'sim':self.sim}

	def command(self, commands = ['None']):
		def decorator(funk):
			for x in commands:
				self.commands[x] = funk
		return decorator

class PluginManager(object):
	"""docstring for PluginManager"""
	def __init__(self):
		self.LoadedPlugins = []
		self.AdminsPlugins = []

	def Load(self, plugin_dir, settings):
		check('folder', plugin_dir)
		print('[plugin] clear lists... |', end='')
		self.LoadedPlugins.clear()
		self.AdminsPlugins.clear()
		files = []
		print(f'{Fore.GREEN}complete{Fore.RESET}')
		
		# scan plugins
		ss = os.listdir(plugin_dir) # Получаем список плагинов в /plugins
		sys.path.insert( 0, plugin_dir) # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить
		
		# import plugins
		print('[plugin] importing plugins...')
		for s in ss:
			ignored = False
			for x in settings['ignored_files']:
				if x == s:
					ignored = True
			if not ignored:
				print (f'detect: {Fore.BLUE}{s}{Fore.RESET}')
				file = __import__(os.path.splitext(s)[ 0], None, None, ['']) # Импортируем исходник плагина
				files.append(file)
		print('[plugin] loading...')
		
		# add plugins
		for plugin in files:
			# check on list 'plugins'
			tier = 0
			data = plugin.data # Вызываем событие загруки этого плагина
			admin = ''
			name = data['name']
			preffix = data['preffix']
			usage = data['usage']
			sim = data['sim']
			commands = data['commands']
			cc = len(usage)
			for x in settings['admin_plugins']:
				if x == '*' or x == data['name']:
					tier = 1
					admin = 'ADMIN'
					self.LoadedPlugins.append(plugin)
					LoadedPluginsData.append({'commands':commands, 'tier':tier, 'name':name, 'preffix':preffix, 'usage':usage, 'sim':sim})
					print(f'{Fore.RED}{admin}{Fore.MAGENTA}> {Fore.GREEN}{name} {Fore.YELLOW}preffix: {Fore.CYAN}{preffix} {Fore.YELLOW}commands: {Fore.RED}{cc} {Fore.RESET}|')
			for x in settings['plugins']:
				if x == '*' or x == data['name']:
					if tier == 0:
						self.LoadedPlugins.append(plugin)
						LoadedPluginsData.append({'tier':tier, 'name':name, 'preffix':preffix, 'usage':usage, 'sim':sim})
						print(f'{Fore.RED}{admin}{Fore.MAGENTA}> {Fore.GREEN}{name} {Fore.YELLOW}preffix: {Fore.CYAN}{preffix} {Fore.YELLOW}commands: {Fore.RED}{cc} {Fore.RESET}|')
		print(f'[pl.sys] complete:')

	def answer(self, data, cmd, arg, admins = False):
		settings = load_settings()
		if admins:
			is_blocked = check_role('black_list', data['from_id'])
			admin = utils.check_role('admins_list', data['from_id'])
		else:
			is_blocked = False
			admin = False

		if not is_blocked:
			for p in LoadedPluginsData:
				preffix = p['preffix']
				commands = p['commands']
				tier = p['tier']
				if admin or data['from_id'] == settings['main_admin']:
					if preffix == cmd:
						for c in commands:
							if arg == c:
								commands[c](data, arg)
				else:
					if tier == 0:
						if preffix == cmd:
							for c in commands:
								if arg == c:
									commands[c](data, arg)
			print(f'{Fore.GREEN}complete{Fore.RESET}')
		else:
			print(f'{Fore.RED}ignored{Fore.RESET}')