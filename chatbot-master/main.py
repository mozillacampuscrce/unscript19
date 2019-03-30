from flask import Flask, render_template, request, jsonify, redirect
import aiml
from twilio.rest import Client
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
from twilio import twiml

app = Flask(__name__)


title = "Medical help app"
heading = "Application for medical help"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.MedicalApp    #Select the database
pat = db.patients #Select the collection name
"""
def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index') """

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = pat.find()
	a1="active"
	return render_template('index.html',a1=a1,pat=todos_l,t=title,h=heading,db = pat)

@app.route("/")
def hello():
	return render_template('login.html')

@app.route("/action", methods=['POST'])
def action ():
	#Adding a patient data
	name=request.values.get("name")
	gender=request.values.get("gender")
	dob=request.values.get("dob")
	contact=request.values.get("contact")
	ms=request.values.get("ms")
	age=request.values.get("age")
	nextVisit=request.values.get("nextVisit")
	doctor_name=request.values.get("doctor_name")
	contact_info=request.values.get("contact_info")
	medicine_name=request.values.get("medicine_name")
	pat.insert({"name":name,"gender":gender,"dob":dob,"contact":contact,"maritalstatus":ms,"Age":age,"Vists":nextVisit,"assigned_doctors":{"name":doctor_name,"contact_info":contact_info,"specialization":"MBBS"},"medication":{"medicine_name":medicine_name,"dosage":"5mg","dosage_interval":"3","first_dosage":"09:00:00","dosage_count":"4"},"exercises":{"exercise_name":"Shavasan","exercise_link":"","exercise_time":"06:30:00"}});
	return redirect(url_for('/chat'))

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	pat.remove({"_id":ObjectId(key)})
	return redirect("/list")


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    resp = twiml.Response()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    return str(resp)



@app.route("/chat")
def chats():
    return render_template('chat.html')

@app.route("/validate",methods = ['POST'])
def checkValid():
	#return redirect("/chat")
	#9821593690 #
	username = request.values.get("login")
	password = request.values.get("password")
	print(username)
	print(password)
	pwd="Hi"
	#pwd = pat.find({"contact":username})
	if pwd=="Hi":
		return redirect("/chat")
	else:
		return "Wrong"

@app.route("/ask", methods=['POST'])
def ask():
	message = request.form['messageText'].encode('utf-8').strip()

	kernel = aiml.Kernel()
	if os.path.isfile("bot_brain.brn"):
	    kernel.bootstrap(brainFile = "bot_brain.brn")
	else:
	    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	    kernel.saveBrain("bot_brain.brn")

	# kernel now ready for use
	while True:
		distress = str(message)
		distress = distress[2:len(distress)-1]
		print(distress)
		if distress.split(' ')[0] == "call":
			receiver = distress.split(' ')[1]
			print(receiver)
			account_sid = "ACead452ce756e314717f4cee6e0cac0c7"
			auth_token = "36308443a7f8388787f4e4f9969bc6fc"
			# (201) 817-4840 Twilio number
			client = Client(account_sid,auth_token)
			call = client.calls.create(
					to = "+919821593690",
					from_ = "+12018174840",
					url = "http://demo.twilio.com/docs/voice.xml"
				)
			print(call.sid)
			
		if message == "quit":
			exit()
		elif message == "save":
			kernel.saveBrain("bot_brain.brn")
		else:
			b = message.decode('utf-8')
			print(b+"decoded msg")
			bot_response = kernel.respond(b)
			# type(bot_response)
			print(bot_response)
			return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
