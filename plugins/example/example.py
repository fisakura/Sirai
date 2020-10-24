# ----- < import > -----
from core.plugin import Plugin
from core.utils import write_msg

plugin = Plugin('example', '/example', ['test - тестовая комманда'], '⚪')
data = plugin.plugin_data

@plugin.command(['test'])
def test(data, arg):
	write_msg(data, 'hello world!')