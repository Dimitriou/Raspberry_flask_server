
import RPi.GPIO as GPIO
from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define sensors GPIOs
button = 18
senPIR = 23
#define actuators GPIOs
outpin1 = 21
outpin2 = 20
outpin3 = 16
outpin4 = 26
#initialize GPIO status variables
buttonSts = 0
senPIRSts = 0
outpin1Sts = 0
outpin2Sts = 0
outpin3Sts = 0
outpin4Sts = 0
#define inputs and outputs
GPIO.setup(button, GPIO.IN)
GPIO.setup(senPIR, GPIO.IN)

GPIO.setup(outpin1, GPIO.OUT)
GPIO.setup(outpin2, GPIO.OUT)
GPIO.setup(outpin3, GPIO.OUT)
GPIO.setup(outpin4, GPIO.OUT)
#turn outputs off
GPIO.output(outpin1, GPIO.HIGH)
GPIO.output(outpin2, GPIO.HIGH)
GPIO.output(outpin3, GPIO.HIGH)
GPIO.output(outpin4, GPIO.HIGH)


app.secret_key="motherfucker"


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/info")
def info():
	return render_template("info.html")


@app.route("/projects")
def projects():
	return render_template("projects.html")


@app.route("/log in", methods=["POST", "GET"])
def log():
	if request.method == "POST":
		pswrd = request.form["nm"]
		if pswrd == '123456':
			session["pswrd"]=pswrd
			login=1
			session["login"]=login

			return redirect(url_for("panel"))
		else:
			login=0
			session["login"]=login			
			return render_template("log.html")

	else:
		return render_template("log.html")


@app.route("/power_supply")
def power_supply():
	return render_template("power_supply.html")


@app.route("/buck")
def buck():
	return render_template("buck.html")


@app.route("/zero_cross_230")
def zero_cross_230():
	return render_template("zero_cross_230.html")


@app.route("/tesla_coil")
def tesla_coil():
	return render_template("tesla_coil.html")


@app.route("/panel", methods=["POST", "GET"])
def panel():

	if request.method == "POST" and "pswrd" in session:

		pswrd=session["pswrd"]
		login=session["login"]
		if login == 1:
			logmsg=1
		else:
			logmsg=0

		g=open("start.txt", "r+")
		nums=g.readlines()
		nums=[int(e) for e in nums]
		g.close()
		i=nums[0]
		j=nums[1]
		k=nums[2]
		l=nums[3]

		if request.form.get('subject') == '10':
			i=10
			GPIO.output(outpin1, GPIO.HIGH)
			print("10")
		elif request.form.get('subject') == '11':
			i=11
			GPIO.output(outpin1, GPIO.LOW)
			print("11")

		if request.form.get('subject') == '20':
			j=20
			GPIO.output(outpin2, GPIO.HIGH)
			print("20")
		elif request.form.get('subject') == '21':
			j=21
			GPIO.output(outpin2, GPIO.LOW)
			print("21")
		
		if request.form.get('subject') == '30':
			k=30
			GPIO.output(outpin3, GPIO.HIGH)
			print("30")
		elif request.form.get('subject') == '31':
			k=31
			GPIO.output(outpin3, GPIO.LOW)
			print("31")

		if request.form.get('subject') == '40':
			l=40
			GPIO.output(outpin4, GPIO.HIGH)
			print("40")
		elif request.form.get('subject') == '41':
			l=41
			GPIO.output(outpin4, GPIO.LOW)
			print("41")

		f=open("start.txt","w")
		f.write('%d\n' % i )
		f.write('%d\n' % j )
		f.write('%d\n' % k )
		f.write('%d\n' % l )
		f.close()

		return render_template("panel.html", i=i, j=j, k=k, l=l, logmsg=logmsg)
	
	elif "pswrd" in session:

		g=open("start.txt", "r+")
		nums=g.readlines()
		nums=[int(e) for e in nums]
		g.close()
		i=nums[0]
		j=nums[1]
		k=nums[2]
		l=nums[3]

		login=session["login"]
		if login == 1:
			logmsg=1
		else:
			logmsg=0

		return render_template("panel.html", i=i, j=j, k=k, l=l, logmsg=logmsg)

	else:

		g=open("start.txt", "r+")
		nums=g.readlines()
		nums=[int(e) for e in nums]
		g.close()
		i=nums[0]
		j=nums[1]
		k=nums[2]
		l=nums[3]

		return render_template("panel.html", i=i, j=j, k=k, l=l)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)

