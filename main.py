from pypresence import Presence
import sys
import codecs
import time
import random
import json

version = "1.0"
creator = "das Alex#2023"


def cfg_open(file:str,name:str):
	try:
		f = codecs.open(file, "r", "utf-8")
	except:
		error(f"Не вдалося знайти файл: {file}")
		return
	
	for line in f:
		if " = " in line:
			key = line.split(" = ")[0]
			value = line.split(" = ")[1]
		elif "=" in line:
			key = line.split("=")[0]
			value = line.split("=")[1]
		else: key = "__none__"
		
		if key == name and key != "__none__":
			return value.replace("\n","").replace("\r","")
	
	error(f'Не вдалося знайти параметр, під назвою \"{name}\"')
	return

def error(text:str="Сталася невідома помилка!"):
	print(text)
	input("Натисніть будь-яку клавішу, щоб вийти . . . ")
	sys.exit()

try:
	client_id = int(cfg_open('config.cfg','client_id'))
except: error('Параметр \"client_id\" повинен бути цілим числом!')

try:
	update_rate = int(cfg_open('config.cfg','update_rate'))
	if update_rate < 15: update_rate = 15
except: error('Параметр \"update_rate\" повинен бути цілим числом!')

statuses_file = cfg_open('config.cfg','statuses_file')

try:
	status_type = int(cfg_open('config.cfg','status_type'))
except: error('Параметр \"status_type\" повинен бути цілим числом!')

status_name = cfg_open('config.cfg','status_name')


print(f"AdvRPC v{version} успішно запущено!\nРозробник: {creator}")
try:
	RPC = Presence(client_id)
	RPC.connect()
except:
	error("Не вдалося запустити RPC. (Можливо ви вказали не вірний Client ID)")

def update_status():
	try:
		with open(statuses_file, "r",encoding='utf-8') as f: statuses = json.load(f)
	except: error(f"Не вдалося відкрити файл: {statuses_file}")
	
	if status_type == 1: status = statuses[random.choice(list(statuses.keys()))]
	elif status_type == 2:
		try: status = statuses[status_name]
		except: error(f'Не вдалося знайти вказаний статус \"{status_name}\"!')
	else: status = statuses[list(statuses.keys())[0]]
	
	if "large_image" in status:
		if status["large_image"].lower() == "none": status["large_image"] = None
	else: status["large_image"] = None
	
	if "large_text" in status:
		if status["large_text"].lower() == "none": status["large_text"] = None
	else: status["large_text"] = None
	
	if "small_image" in status:
		if status["small_image"].lower() == "none": status["small_image"] = None
	else: status["small_image"] = None
	
	if "small_text" in status:
		if status["small_text"].lower() == "none": status["small_text"] = None
	else: status["small_text"] = None
	
	if "buttons" in status:
		if len(status["buttons"]) < 1: status["buttons"] = None
	else: status["buttons"] = None

	if "timer" in status:
		if status["timer"].lower() == "true": status["timer"] = int(time.time())
		else: status["timer"] = None
	else:
		status["timer"] = None
	if status_type == 1:
		status["timer"] = None

	RPC.update(
		details=status["details"],
		state=status["state"],
		large_image=status["large_image"],
		large_text=status["large_text"],
		small_image=status["small_image"],
		small_text=status["small_text"],
		start=status["timer"],
		buttons=status["buttons"]
	)

try:
	with open(statuses_file, "r",encoding='utf-8') as f: statuses = json.load(f)
except: error(f"Не вдалося відкрити файл: {statuses_file}")

if status_type == 1: status = statuses[random.choice(list(statuses.keys()))]
elif status_type == 2:
	try: status = statuses[status_name]
	except: error(f'Не вдалося знайти вказаний статус \"{status_name}\"!')
else: status = statuses[list(statuses.keys())[0]]

if status_type != 1 and status["timer"].lower() == "true":
	update_status()
	while True:
		time.sleep(update_rate)
else:
	while True:
		update_status()
		time.sleep(update_rate)