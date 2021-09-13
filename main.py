
import re ,sys
import json 
import random
import requests 
from clint.textui import puts , colored , indent 
import argparse 
import names 
import concurrent.futures 
from random_username.generate import generate_username
from user_agent import generate_user_agent




parser = argparse.ArgumentParser()
parser.add_argument("-s",  help="single email check ")
parser.add_argument("-m", help="multiple email check")
parser.add_argument("-g", help="generate and check without user interference")
parser.add_argument("-g2", help="generate and check without user interference")
parser.add_argument("-t", help="threaded ")
args = parser.parse_args()






lst = [] 
tmp = []

def mail_gen2(n):
	''' A function to generate mails  '''
	
	lst = [ item+"@outlook.com" for item in generate_username(n) ]

	return lst 



def mail_gen(n):
	''' a function to generate emails  '''
	full_name = names.get_full_name()
	first , last = full_name.split()

	
	tmp = [ first+str(i)+"@outlook.com" for i in range (n) ]

	return tmp






def check_outlook(mail):

	# if value is 1 user is invalid 
	reg = r'IfExistsResult\":1'

	## if value is 0 then user is valid 
	reg2 = r'IfExistsResult\":0'

	data = {
		'username':f'{mail}'
	}

	payload = {"User-Agent":generate_user_agent()}

	resp = requests.get("http://login.live.com", data, headers=payload)
	
	#print (resp.status_code)
	cleanreg = re.compile('<.*?>')	

	clean_text = re.sub(cleanreg , '' , resp.text)
	res = re.findall(reg, resp.text)
	res2 = re.findall(reg2, resp.text)

	if len(res) > 0:
		puts( colored.red(f" [ {mail} ] is not valid"))

	elif len(res2) > 0:
		puts(colored.green(f" [ {mail} ] is valid"))
		lst.append(mail)




def load_emails(file_name):
	with open(file_name, 'r') as handler:
		return list(handler)




def create_output(lst):
	''' writes found emails to a txt file'''
	with open('output.txt' , 'a') as f:
		for item in lst:
			f.write(item+"\n")



if __name__ == "__main__":
	
	if args.s :
		check_outlook(args.s)



	if args.m: 
		file_name = args.m
		try:

			with open(args.m , 'r') as handler:
				for item in handler:
					check_outlook(item)
		except FileNotFoundError as no_file:
			print (f"{args.m} not found !!!")


	if args.g:
		
		tmp = mail_gen(int(args.g))
		if not args.t:

			
			print (f" Total generated mails : {len(tmp)} ")
			for item in tmp:
				check_outlook(item)
		else:
			with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.t)) as executor:
				results = {executor.submit(check_outlook , item ): item for item in tmp }
				for future in concurrent.futures.as_completed(results):
					out = results[future]



	if args.g2:
		tmp = mail_gen2(int(args.g2))
		if not args.t:

			
			
			print (f" Total generated mails : {len(tmp)} ")
			for item in tmp:
				check_outlook(item)
		else:
			with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.t)) as executor:
				resutls = {executor.submit(check_outlook , item): item for item in tmp}
				for future in concurrent.futures.as_completed(resutls):
					out = resutls[future]




	print (f"Found {len(lst)} valid emails out of {len(tmp)}")


	create_output(lst)
