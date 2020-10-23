# sirai
бот для вк с поддержкой плагинов

## информация
**версия бота**: v0.1 alpha 

## зависимости
возможные команды для установки модулей
```
pip instal -r requments.txt
python -m pip install -r requments.txt

pip3 install -r requments.txt
python3 -m pip install -r requments.txt
```

## первый запуск и настройка
1. после загрузки репозитория и его распаковки вам необходимо создать файл запуска с любым названием, напртиер `run.py`.
2. в только что созданный файл пока что вписываем, это надо для того чтьобы бот создал файл настроек:
```py
from core.sirai import Sirai # импортируем бота

app = Sirai() # создаём экземпляр класса бота
```
3. отлично, настроим бота. файл намтроек будет выглядеть примерно так
```json
{
    "token": "press token here", // токен для авторизации в вк
    "group_id": "press group id here", // id группы ботв, тоже для авторизации
    "main_chat": 0, // главный чат peer_id (например 2000000001)
    "main_admin": 0, // главный администратор бота, ваш id
    "plugins": [ // список импортируемых имён плагинов
        "*" // все плагины
    ],
    "admin_plugins": [], // список плагинов для администраторов бота
    "ignored_files": [ // список игнорируемых файлов при импорте
        "__pycache__" // python кэш 
    ]
}
```
4. после того как бот настроен, можно дописать файл запуска
```py
from core.sirai import Sirai

app = Sirai(True) # апгумент True означает что мы готовы подключится к вк 
app.load('plugins') # загрузка плагинов из папки plugins, если её нет он её создаст
app.banner() # показать баннер (не обязательно)
app.print_settings() # показать настройки бота
app.run() # запустить цикл обработчика
```
или, если нуюно только главное
```py
from core.sirai import Sirai

app = Sirai(True) 
app.load('plugins')
app.run()

```
готово :)

## создание плагинов
наверное самым важныи аспектом бота являются **плагины**

простой плагин выглядет так:
```py
# ----- < import > -----
from core.plugin import Plugin # импортируем класс плагина
from core.utils import write_msg # импортируем метод отправки сообщения

plugin = Plugin('example', '/example', ['test - тестовая комманда'], '⚪') # создаём плагин
data = plugin.plugin_data # переменная имформации о плагине

@plugin.command(['test']) # создаём команду '/example test'
def test(data, arg): # функция команды
    write_msg(data, 'hello world!') # отправляем обратно текст 'hello world!'
```
при вызове команды **/example test** бот отправит сообщенте с текстом **hello world!**