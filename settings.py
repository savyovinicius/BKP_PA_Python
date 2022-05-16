import click
import configparser
import requests
import urllib.parse
import re
from os.path import exists

CFG_FILE="settings.cfg"
parser = None

def get_key(api_server, api_root, key_param):
	return 0

@click.command()
@click.option(
	'--api_server',
	prompt="IP ou Dominio do Palo Alto",
	help="IP ou Dominio do servidor de API do Palo Alto"
	)
def set_api_server(api_server):
	parser.set("API","api_server",api_server)
	with open(CFG_FILE, 'w') as file:
		parser.write(file)

	if(not parser.has_option("API","api_key")):
		set_api_key()

@click.command()
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def set_api_key(user,password):
	api_server = parser.get("API","api_server")
	api_root = parser.get("API","api_root")
	user = urllib.parse.quote(user)
	password = urllib.parse.quote(password)

	api_url = f"https://{api_server}/{api_root}/?type=keygen&user={user}&password={password}"
	response = requests.get(api_url, verify=False)
	content = response.content.decode("utf-8")
	content = re.sub('<[a-z/="\' ]+>', '', content)
	parser.set("API","api_key",content)
	with open(CFG_FILE, 'w') as file:
		parser.write(file)

@click.command()
@click.option(
	'--api_root',
	default="api",
	help="Caminho da raiz da API"
	)
@click.option(
	'--cfg_param',
	default="type=export&category=configuration",
	help="Parametros usados na requisicao para exportar a configuracao vigente"
	)
@click.option(
	'--log_path',
	default="",
	help="Caminho do diretorio onde serao armazenados os logs"
	)
@click.option(
	'--log_file',
	default="historico.log",
	help="Arquivos onde serao armazenados os logs"
	)
@click.option(
	'--retry_delay',
	default=5,
	help="Tempo, em segundos, entre uma requisicao e outra quando ha erro"
	)
@click.option(
	'--max_retries',
	default=3,
	help="Numero maximo de tentativas antes de exportar a configuracao vigente"
	)
def settings(api_root, cfg_param,log_path,log_file,retry_delay,max_retries):
	if exists(CFG_FILE):
		parser.read("settings.cfg")
	else:
		parser.add_section("API")
		parser.add_section("CONFIG")

	#api_key = get_key(api_server, api_root, key_param);
	
	#parser.set("API","api_server",api_server)
	parser.set("API","api_root",api_root)
	parser.set("API","cfg_param",cfg_param)
	#parser.set("API","api_key",api_key)

	parser.set("CONFIG","log_path",log_path)
	parser.set("CONFIG","log_file",log_file)
	parser.set("CONFIG","retry_delay",str(retry_delay))
	parser.set("CONFIG","max_retries",str(max_retries))

	with open(CFG_FILE, 'w') as file:
		parser.write(file)

	if(not parser.has_option("API","api_server")):
		set_api_server()
	elif(not parser.has_option("API","api_key")):
		set_api_key()
	



if __name__ == '__main__':
	parser = configparser.ConfigParser()
	settings()