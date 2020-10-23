import datetime
import os
from vk_api.utils import get_random_id
from colorama import Fore
import colorama
import json
import vk_api
import random
import re
import math
import vk_api
colorama.init()

def date():
	b = colors['b']
	re = colors['re']
	t = datetime.datetime.now()
	t = t.strftime('%c')
	text = f'[{b}{t}{re}]'
	return text

def check(mode, data, text=''):
	if not os.path.exists(data):
		if mode == 'folder':
			os.mkdir(data)
			print(f'{date()} {Fore.GREEN} создана дирректория {data}{Fore.RESET}')
		if mode == 'file':
			with open(data, 'w') as f:
				f.write(text)
				print(f'{date()} {Fore.GREEN} создан файл {data}{Fore.RESET}')

def load_settings():
	settings = {'token':'press token here',
				'group_id':'press group id here',
				'main_chat':0,
				'main_admin': 0,
				'plugins':["*"],
				'admin_plugins':[],
				'ignored_files':['__pycache__']}
	check('file', 'settings.json',json.dumps(settings, indent=4))
	with open('settings.json') as f:
		data = json.load(f)
	return data

# colors
colors = {'r':Fore.RED, 'y':Fore.YELLOW, 'g':Fore.GREEN, 'c':Fore.CYAN, 'b':Fore.BLUE, 'm':Fore.MAGENTA, 're':Fore.RESET}
settings = load_settings()
vk = vk_api.VkApi(token=settings['token'])

# send message from vk
def write_msg(data, message):
	vk.method('messages.send', {'peer_id': data['peer_id'], 'message': message, 'random_id': get_random_id()})

def check_role(list_name, user_id, folder='admin-tools'):
	has_role = False
	with open(f'{folder}/{list_name}.json') as f:
		data = json.load(f)
	for x in data:
		if x == user_id:
			has_role = True
	return has_role

def list_manager(mode, list_name, user_id='', folder='admin-tools'):
	if mode == 'add':
		with open(f'{folder}/{list_name}.json') as f:
			filedata = json.load(f)
		if filedata == 'hello':
			filedata = []
		filedata.append(user_id)
		with open(f'{folder}/{list_name}.json', 'w') as f:
			f.write(json.dumps(filedata))
		print(f'пользователь {Fore.GREEN}{user_id}{Fore.RESET} добавлен в спиок {Fore.MAGENTA}{list_name}')
	
	if mode == 'remove':
		with open(f'{folder}/{list_name}.json') as f:
			filedata = json.load(f)
		filedata.remove(user_id)
		with open(f'{folder}/{list_name}.json', 'w') as f:
			f.write(json.dumps(filedata))
		print(f'пользователь {Fore.GREEN}{user_id}{Fore.RESET} удалён из списка {Fore.MAGENTA}{list_name}')


cases = (2, 0, 1, 1, 1, 2)
def plural_form(n: int, v: (list, tuple)):
	"""Функция возвращает число и просклонённое слово после него

	Аргументы:
	:param n: число
	:param v: варианты слова в формате (для 1, для 2, для 5)

	Пример:
	plural_form(difference.days, ("день", "дня", "дней"))

	:return: Число и просклонённое слово после него
	"""

	return f"{n} {v[2 if (4 < n % 100 < 20) else cases[min(n % 10, 5)]]}"

# ----- < game bot > -----

users_dir = "game/users"

def loadjson(filepath):
	with open(filepath, encoding='utf-8') as jsonfile:
		return json.load(jsonfile, encoding='utf-8')

def dumpjson(data, filepath):
	with open(filepath, 'w', encoding='utf-8') as jsonfile:
		return json.dump(data, jsonfile, ensure_ascii=False)

def check_casino_win(user_id):
	read_file = open(users_dir + str(user_id) + ".json", "r", encoding='utf-8')
	get_data = json.load(read_file, encoding='utf-8')
	read_file.close()
	donate_group = get_data['group']
	chance = math.ceil(random.randint(1, 100) / 33.0000)
	if donate_group == 'VIP':
		pass_count = 1
		while chance != 1 and pass_count:
			chance = math.ceil(random.randint(1, 100) / 33.0000)
			pass_count -= 1
	elif donate_group == 'Premium':
		pass_count = 2
		while chance != 1 and pass_count:
			chance = math.ceil(random.randint(1, 100) / 33.0000)
			pass_count -= 1
	else:
		pass_count = 0
		while chance != 1 and pass_count:
			chance = math.ceil(random.randint(1, 100) / 33.0000)
			pass_count -= 1
	return chance

def check_word_monetka(word):
	if str(word) == 'орёл':
		return 1
	elif str(word) == 'орел':
		return 1
	elif str(word) == 'решка':
		return 2

def check_word_traid(word):
	if str(word) == 'вверх':
		return 1
	elif str(word) == 'вниз':
		return 2

def convert_win_monetka(chislo_rand):
	if int(chislo_rand) == 1:
		return 'Выпал: Орел'
	elif int(chislo_rand) == 2:
		return 'Выпала: Решка'

def ruda_price_salem(col_ruda, price_ruda):
	if col_ruda > 1:
		algo = col_ruda * price_ruda
		return algo
	else:
		return 0

def check_group(id):
	get_data = loadjson(f'{users_dir}/{id}.json')
	donate_group = get_data['group']
	if get_data['group'] == 'Player':
		donate_group = '🔰 Привилегия: Игрок'
	elif get_data['group'] == 'VIP':
		donate_group = '⚜ Привилегия: ВИП'
	elif get_data['group'] == 'Premium':
		donate_group = '🔱 Привилегия: Премиум'
	return donate_group

def check_nick(id):
	get_data = loadjson(f'{users_dir}/{id}.json')
	user_nick = get_data['user_nick']
	if get_data['user_nick'] == 'None':
		user_nick = 'Не установлен'
		return user_nick
	else:
		return user_nick

def check_own_housing(own_housing):
	if own_housing == 0:
		return ''
	elif own_housing == 1:
		return '⠀⠀🏠 Коробка\n'
	elif own_housing == 2:
		return '⠀⠀🏠 Подвал\n'
	elif own_housing == 3:
		return '⠀⠀🏠 Сарай\n'
	elif own_housing == 4:
		return '⠀⠀🏠 Гараж\n'
	elif own_housing == 5:
		return '⠀⠀🏠 Ветхая хижина\n'
	elif own_housing == 6:
		return '⠀⠀🏠 Деревянный доми\n'
	elif own_housing == 7:
		return '⠀⠀🏠 Кирпичный дом\n'
	elif own_housing == 8:
		return '⠀⠀🏠 Коттедж\n'
	elif own_housing == 9:
		return '⠀⠀🏠 Дом на Пумавуде\n'
	elif own_housing == 10:
		return '⠀⠀🏠 Вилла на Пумавуде\n'
	elif own_housing == 11:
		return '⠀⠀🏠 Личный остров\n'
	elif own_housing == 30:
		return '⠀⠀🏠 Секретное жильё\n'

def check_own_car(own_car):
	if own_car == 0:
		return ''
	elif own_car == 1:
		return '⠀⠀🚗 Велосипед\n'
	elif own_car == 2:
		return '⠀⠀🚗 Гироскутер\n'
	elif own_car == 3:
		return '⠀⠀🏍 Ducati Scrambler\n'
	elif own_car == 4:
		return '⠀⠀🏍 Honda CTX1300\n'
	elif own_car == 5:
		return '⠀⠀🚗 Ferrari California front\n'
	elif own_car == 6:
		return '⠀⠀🚗 Porsche 911\n'
	elif own_car == 7:
		return '⠀⠀🚗 Nissan GT-R\n'
	elif own_car == 8:
		return '⠀⠀🚗 BMW X6\n'
	elif own_car == 9:
		return '⠀⠀🚗 Jaguar F-Type\n'
	elif own_car == 10:
		return '⠀⠀🚗 Lamborghini Huracán\n'
	elif own_car == 11:
		return '⠀⠀🚗 Lamborghini Gallardo\n'
	elif own_car == 12:
		return '⠀⠀🚗 Ferrari F80 Concept\n'
	elif own_car == 13:
		return '⠀⠀🚗 Lamborghini Sesto\n'
	elif own_car == 14:
		return '⠀⠀🚗 Various Ford-based trucks\n'
	elif own_car == 15:
		return '⠀⠀🚗 Tesla Cybertruck\n'
	elif own_car == 30:
		return '⠀⠀🚗 Секретная машина\n'

def check_own_yacht(own_yacht):
	if own_yacht == 0:
		return ''
	elif own_yacht == 1:
		return '⠀⠀🛥 RHIB\n'
	elif own_yacht == 2:
		return '⠀⠀🛥 Kawasaki\n'
	elif own_yacht == 3:
		return '⠀⠀🛥 Riva Aquarama\n'
	elif own_yacht == 4:
		return '⠀⠀🛥 Various\n'
	elif own_yacht == 5:
		return '⠀⠀🛥 Рrinсеss 60\n'
	elif own_yacht == 6:
		return '⠀⠀🛥 Аzimut 70\n'
	elif own_yacht == 7:
		return '⠀⠀🛥 Dоminаtоr 40M\n'
	elif own_yacht == 8:
		return '⠀⠀🛥 Mооnеn 124\n'
	elif own_yacht == 9:
		return '⠀⠀🛥 Widеr 150\n'
	elif own_yacht == 10:
		return '⠀⠀🛥 Palmer Jоhnsоn 42M SuреrSроrt\n'
	elif own_yacht == 11:
		return '⠀⠀🛥 Widеr 165\n'
	elif own_yacht == 12:
		return '⠀⠀🛥 Есliрsе\n'
	elif own_yacht == 13:
		return '⠀⠀🛥 Dubаi\n'
	elif own_yacht == 14:
		return '⠀⠀🛥 Strееts оf Mоnасо\n'
	elif own_yacht == 30:
		return '⠀⠀🛥 Секретная яхта\n'

def check_own_air(own_air):
	if own_air == 0:
		return ''
	elif own_air == 1:
		return '⠀⠀✈ de Havilland Canada DHC-2\n'
	elif own_air == 2:
		return '⠀⠀✈ Piper PA-46\n'
	elif own_air == 3:
		return '⠀⠀✈ Cessna 310\n'
	elif own_air == 4:
		return '⠀⠀✈ Learjet 55\n'
	elif own_air == 5:
		return '⠀⠀✈ Bombardier Global Express\n'
	elif own_air == 6:
		return '⠀⠀✈ Cessna Citation X\n'
	elif own_air == 7:
		return '⠀⠀✈ C-130\n'
	elif own_air == 8:
		return '⠀⠀✈ VOLATOL\n'
	elif own_air == 9:
		return '⠀⠀✈ RM-10 BOMBUSHKA\n'
	elif own_air == 10:
		return '⠀⠀✈ AVENGER — HYV\n'
	elif own_air == 11:
		return '⠀⠀✈ F-16 Fighting Falcon\n'
	elif own_air == 12:
		return '⠀⠀✈ RM-10 BOMBUSHKA\n'
	elif own_air == 13:
		return '⠀⠀✈ TULA — MAMMOTH\n'
	elif own_air == 14:
		return '⠀⠀✈ V-65 MOLOTOK\n'
	elif own_air == 15:
		return '⠀⠀✈ MOGUL — MAMMOTH\n'
	elif own_air == 30:
		return '⠀⠀✈ Секретный самолёт\n'

def check_own_helicopter(own_helicopter):
	if own_helicopter == 0:
		return ''
	elif own_helicopter == 1:
		return '⠀⠀🚁 Eurocopter EC130/135/14\n'
	elif own_helicopter == 2:
		return '⠀⠀🚁 Boeing MH-6\n'
	elif own_helicopter == 3:
		return '⠀⠀🚁 Sikorsky UH-60\n'
	elif own_helicopter == 4:
		return '⠀⠀🚁 HAVOK — NAGASAKI\n'
	elif own_helicopter == 5:
		return '⠀⠀🚁 Eurocopter EC145\n'
	elif own_helicopter == 6:
		return '⠀⠀🚁 Airbus H160\n'
	elif own_helicopter == 7:
		return '⠀⠀🚁 Mil Mi-24\n'
	elif own_helicopter == 8:
		return '⠀⠀🚁 POLICE MAVERICK\n'
	elif own_helicopter == 9:
		return '⠀⠀🚁 MAVERICK\n'
	elif own_helicopter == 30:
		return '⠀⠀🚁 Секретный вертолёт\n'

def check_own_comp(own_comp):
	if own_comp == 0:
		return ''
	elif own_comp == 1:
		return '⠀⠀🖥 Book\n'
	elif own_comp == 2:
		return '⠀⠀🖥 Book Air\n'
	elif own_comp == 3:
		return '⠀⠀🖥 Book Pro\n'

def check_own_smart(own_smart):
	if own_smart == 0:
		return ''
	elif own_smart == 1:
		return '⠀⠀📱 iPhone\n'
	elif own_smart == 2:
		return '⠀⠀📱 iPhone Pro\n'
	elif own_smart == 3:
		return '⠀⠀📱 iPhone Pro Max\n'

def check_own_farm(own_farm):
	if own_farm == 0:
		return ''
	elif own_farm == 1:
		return '⠀⠀🔋 Miner\n'
	elif own_farm == 2:
		return '⠀⠀🔋 Miner S\n'
	elif own_farm == 3:
		return '⠀⠀🔋 Miner X\n'

def check_own_profile(id):
	get_data = loadjson(f'{users_dir}/{id}.json')
	own_housing = int(get_data['own_housing'])
	own_car = int(get_data['own_car'])
	own_yacht = int(get_data['own_yacht'])
	own_air = int(get_data['own_air'])
	own_helicopter = int(get_data['own_helicopter'])
	own_comp = int(get_data['own_comp'])
	own_smart = int(get_data['own_smart'])
	own_farm = int(get_data['own_farm'])
	if own_housing >= 1:
		return '\n\n🔑 Имущество:\n'
	elif own_car >= 1:
		return '\n\n🔑 Имущество:\n'
	elif own_yacht >= 1:
		return '\n\n🔑 Имущество:\n'
	elif own_air >= 1:
		return '\n\n🔑 Имущество:\n'
	elif own_helicopter >= 1:
		return '\n\n🔑 Имущество:\n'
	elif own_comp >= 1:
		return '\n\n🔑 Имущество:\n'
	elif own_smart >= 1:
		return '\n\n🔑 Имущество:\n'
	elif own_farm >= 1:
		return '\n\n🔑 Имущество:\n'
	else:
		return ''

def removeLink(text):
	try:
		text = re.sub('@', '', text)
		text = re.sub('https://vk.com/', '', text)
		text = re.sub('https://vk.com/id', '', text)
		try:
			text = re.search("id(\\d+)", text).group(1)
		except AttributeError:
			pass

		if text.isdigit():
			return text
		else:
			username = vk.utils.resolveScreenName(screen_name=text)
			if not username:
				pass
			else:
				check_type = username['type']
				if str(check_type) == 'user':
					user_id = str(username['object_id'])
					if user_id.isdigit():
						return int(username['object_id'])
					else:
						pass
				else:
					pass
	except vk_api.exceptions.ApiError:
		pass
	except AttributeError:
		pass

def sendMessageTOid(text, toID):
	vk_session = vk_api.VkApi(token=token)
	vk = vk_session.get_api()
	users_dir = os.path.join(r"users/")

	read_file = open(users_dir + str(toID) + ".json", "r", encoding='utf-8')
	get_data = json.load(read_file, encoding='utf-8')
	read_file.close()
	if get_data['nick'] == '0':
		mention = '@id{}'.format(toID) + '(' + get_data['first_name'] + ')'
	elif get_data['nick'] == '1':
		mention = '@id{}'.format(toID) + '(' + get_data['user_nick'] + ')'
	else:
		mention = '@id{}'.format(toID) + '(' + get_data['first_name'] + ')'
	try:
		vk.messages.send(random_id=random.randint(-2147483648, +2147483648), peer_id=toID, message=mention + text)
	except vk_api.exceptions.ApiError:
		pass

def sendMessageTOid_attachment(text, toID, attachment):
	vk_session = vk_api.VkApi(token=token)
	vk = vk_session.get_api()
	users_dir = os.path.join(r"users/")

	read_file = open(users_dir + str(toID) + ".json", "r", encoding='utf-8')
	get_data = json.load(read_file, encoding='utf-8')
	read_file.close()
	if get_data['nick'] == '0':
		mention = '@id{}'.format(toID) + '(' + get_data['first_name'] + ')'
	elif get_data['nick'] == '1':
		mention = '@id{}'.format(toID) + '(' + get_data['user_nick'] + ')'
	else:
		mention = '@id{}'.format(toID) + '(' + get_data['first_name'] + ')'
	try:
		vk.messages.send(random_id=random.randint(-2147483648, +2147483648), peer_id=toID, attachment=attachment, message=mention + text)
	except vk_api.exceptions.ApiError:
		pass