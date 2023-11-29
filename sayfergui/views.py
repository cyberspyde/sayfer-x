from django.shortcuts import render, redirect
from django.views import View
import json, os
import datetime
from .forms import LoginForm, SettingsForm, EditForm
from django.db import models
from django.views.generic import ListView

knowledgebase_path = 'D:\\Github\\sayferai\\testing\\Knowledge Base'
settings_path = 'D:\\Github\\sayferai\\assets\\settings.conf'
knowledge_conf_path = 'D:\\Github\\sayferai\\assets\\knowledge-configuration.json'

is_logged_in = True
save_login = False
def index(request):
	global is_logged_in, save_login
	if save_login == True:
		return redirect('/dashboard')
	else:
		form = LoginForm()
		if request.method == 'POST':
			form = LoginForm(request.POST)
			print(form.errors)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				saveLoginR = form.cleaned_data.get('saveLogin')
				if username == 'peter' and password == '1234':
					if saveLoginR:
						save_login = True
					is_logged_in = True
					return redirect('/dashboard')

		context = {'form' : form}
		return render(request, '..\\templates\\sayfergui\\index.html', context)

knowledgeBaseFiles = [{'name' : x.split('.')[0]} for x in os.listdir(knowledgebase_path) ]

knowledge_conf = open(knowledge_conf_path, 'r')
knowledge_conf_data = json.load(knowledge_conf)

for i in range(len(knowledgeBaseFiles)):
	knowledgeBaseFiles[i]['id'] = knowledge_conf_data[i]["id"]
	knowledgeBaseFiles[i]['usability'] = knowledge_conf_data[i]["usability"]
	knowledgeBaseFiles[i]['data_count'] = knowledge_conf_data[i]["data_count"]
	knowledgeBaseFiles[i]

global data
def edit(request):
	for k in knowledgeBaseFiles:
		specificKnowledgeBase = k
		file = open(f'{knowledgebase_path}\\{specificKnowledgeBase["name"]}.json', 'r+')
		data = json.load(file)	
		dates = [datetime.datetime.strptime(item['date_updated'], "%Y:%m:%d, %H:%M:%S") for item in data]
		latest_date = max(dates)
		k['last_updated'] = str(latest_date)

	livesearchData = json.dumps(knowledgeBaseFiles)
	context = { 'knowledgeDatabase' : knowledgeBaseFiles, 'livesearchData' : livesearchData}
	return render(request, '..\\templates\\sayfergui\\edit.html', context)

def editKnowledge(request, name):
	for k in knowledgeBaseFiles:
		if k['name'] == name:
			specificKnowledgeBase = k

	file = open(f'{knowledgebase_path}\\{specificKnowledgeBase["name"]}.json', 'rb+')
	data = json.load(file)
	livesearchData = json.dumps(data)
	context = { 'specificKnowledgeBase' : specificKnowledgeBase, 'data' : data, 'name' : name, 'livesearchData' : livesearchData}

	return render(request, '..\\templates\\sayfergui\\editKnowledge.html', context)

def editSpecificKnowledge(request, name, id):
	for k in knowledgeBaseFiles:
		if(k['name']) == name:
			specificKnowledgeBase = k

	file = open(f'{knowledgebase_path}\\{specificKnowledgeBase["name"]}.json', 'rb+')
	data = json.load(file)
	for t in data:
		if t['id'] == id:
			content = t
		
	form = EditForm(initial={"content" : content['content'], "category" : content['category']})
	if request.method == 'POST':
		contentChanged = request.POST['content']
		categoryChanged = request.POST['category']

		for t in data:
			if t['id'] == id:
				t['content'] = contentChanged
				t['category'] = categoryChanged
				t['date_updated'] = datetime.datetime.now().strftime("%Y:%m:%d, %H:%M:%S")
		
		file2 = open(f'{knowledgebase_path}\\{specificKnowledgeBase["name"]}.json', 'w')
		
		json.dump(validate_data(data), file2)
		file2.close()

		return redirect('editKnowledge', name)

	context = {'form' : form}
	return render(request, '..\\templates\\sayfergui\\editSpecificKnowledge.html', context)

def validate_data(input):
		for k in input:
			k['category'] = k['category'].replace('\n', '')
			k['content'] = k['content'].replace('\n', '')
			k['category'] = k['category'].replace('\r', '')
			k['content'] = k['content'].replace('\r', '')
		return input

def dashboard(request):
	global is_logged_in

	settings_raw = open(settings_path, "r")
	settings = json.load(settings_raw)

	gpt3_s = settings['gpt3']
	voice_activation_s = settings['voice_activation']
	robertaqna_s = settings['robertaqna']
	robot_name_s = settings['robot_name']

	settings_raw.close()
	print(gpt3_s)
	

	if is_logged_in:
		form = SettingsForm(initial={"gpt3" : eval(gpt3_s), "robot_name" : robot_name_s, "voice_activation" : eval(voice_activation_s), "robertaqna" : eval(robertaqna_s)})
		if request.method == 'POST':
			form = SettingsForm(request.POST)
			print(form.errors)
			if form.is_valid():
				gpt3 = form.cleaned_data.get('gpt3')
				robertaqna = form.cleaned_data.get('robertaqna')
				voice_activation = form.cleaned_data.get('voice_activation')
				robot_name = form.cleaned_data.get('robot_name')
				settings_raw = open(settings_path, "w")

				data = {
					"voice_activation" : "{}".format(voice_activation),
					"gpt3" : "{}".format(gpt3),
					"robertaqna" : "{}".format(robertaqna),
					"robot_name" : "{}".format(robot_name)
				}

				settings_raw.write(json.dumps(data))
				print("File is written")
				settings_raw.close()
		
		
		context = {'form' : form}
		return render(request, '..\\templates\\sayfergui\\dashboard.html', context)
	else:
		print('User isn`t logged in!')

def test(request):

	return render(request, '..\\templates\\sayfergui\\test.html')

def menu(request):
	return render(request, '..\\templates\\sayfergui\\menu.html')