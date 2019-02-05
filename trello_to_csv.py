import json
import csv
import datetime
import os
from sys import platform

def TrelloToCSV(input_file):

	current_os = platform

	if current_os.startswith("linux"):
		slash = "/"
	elif current_os.startswith("win32") or current_os.startswith("cygwin"):
		slash = "\\"
	elif current_os.startswith("darwin"):
		slash = "/"
	else:
		slash = "/"

	rows = []
	row = ['id','card_name','tags','desc','status','members','creation_time','last_modified','limit_date','completed']
	rows.append(row)

	trello_json = open(input_file, encoding="utf8").read()
	trello_json_parsed = json.loads(trello_json)

	member_rows=[]
	
	for member in trello_json_parsed['members']:
		member_rows.append([member['id'],member['fullName']])
	
	list_rows=[]
	
	for list in trello_json_parsed['lists']:
		list_rows.append([list['id'],list['name']])
	
	for card in trello_json_parsed['cards']:
		id = card['id']
		card_name = card['name']
		
		tags=''
		for tag in card['labels']:
			if tags=='':
				tags=tag['name']
			else:
				tags = '/'.join([tags,tag['name']])
		desc=card['desc']
		
		status=''
		for elem in list_rows:
			if elem[0]==card['idList']:
				status=elem[1]
		
		members=''
		for member in card['idMembers']:
			member_name=''
			for elem in member_rows:
				if elem[0]==member:
					member_name=elem[1]
		
			if members=='':
				members=member_name
			else:
				members='/'.join([members,member_name])
				
		creation_time=datetime.datetime.fromtimestamp(int(id[0:8],16)).isoformat()
		last_modified = card['dateLastActivity']
		limit_date=card['due']
		completed=card['dueComplete']
		rows.append([id,card_name,tags,desc,status,members,creation_time,last_modified,limit_date,completed])
	
	output_file=open(os.getcwd()+slash+'output.csv','w', newline='')
	csvwriter = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
	
	for row_data in rows:
		string_row = ''
		for x in row_data:
			x=str(x).replace("\n","").replace(",","")
			if string_row== '':
				string_row = x
			else:
				string_row=string_row+','+x
		
		
		
		csvwriter.writerow([string_row])
	output_file.close()
	
######################
#        Main        #
######################

if __name__ == "__main__":
    from sys import argv

    TrelloToCSV(argv[1])
