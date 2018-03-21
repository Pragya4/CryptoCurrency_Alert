import select
import psycopg2
import json
import psycopg2.extensions
import smtplib
import string
hostname = 'baasu.db.elephantsql.com'
username = 'dbuzkqmi'
password = 'vi24qSFc5TG77k5GPa4aQr3XlnLOBIRf'
database = 'dbuzkqmi'
port='5432'
conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database,port=port)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
curr = conn.cursor()
curr.execute("LISTEN events;")
collection=[]
print "Waiting for notifications on channel 'myEvent'"
def sendEmail(price,emails):
	from_addr = 'urja4bluestar@gmail.com'
	subject='Alert'
	body_text='Price Change'
	bodytext = string.join(("From: %s" % from_addr,"To: %s" % ', '.join(emails),"Subject: %s" % subject ,"",body_text), "\r\n")

	# Credentials (if needed)
	username = 'akshita311goyal@gmail.com'
	password = '7042031822' 
  
	# The actual mail sent
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(from_addr,emails, bodytext)
	server.quit()
	print("Mail Sent")
		
def checkThresholdAlert(threshold_min,threshold_max,price,userid):
	emails=[]
	if(price < threshold_min or price > threshold_max):
		selectQuery="select email from public.user where user_id={}".format(userid)
		curr.execute(selectQuery)
		result=curr.fetchall()
		if(curr.rowcount != 0):
			for r in result:
				emails.append(r[0])		
			sendEmail(price,emails)

def checkForAlert(collection):
      for i in range(len(collection)):
	   symbol=collection[i]['symbol']
	   #alert_type=collection[i]['alert_type']
	   selectQuery="select * from alert where coin_symbol='{}'".format(symbol)
	   curr.execute(selectQuery)
	   result=curr.fetchall()
	   if(curr.rowcount != 0):
		for r in result:
		    if(r[2] == 'THRESHOLD_ALERT'):
		    	checkThresholdAlert(r[8],r[9],collection[i]['price_usd'],r[1])
while 1:
      conn.poll()
      while conn.notifies:
           notify = conn.notifies.pop(0)
           response=json.loads(notify.payload)
	   jsonObject=response['data']
	   collection.append(jsonObject)
      if len(collection) == 5 : 
	checkForAlert(collection)     	
	collection=[]
	    

