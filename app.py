from flask import Flask, render_template, request, g, session, redirect, url_for, flash
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
app = Flask(__name__)
app.config['SECRET_KEY'] = "KytaRsmbineL2"
app.config['MAIL_USERNAME']='yasinmohammedbest@gmail.com'
app.config['MAIL_PASSWORD']='KairaKishi1'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
class message() :
	def __init__(self, reciptinent, sender, time, content) :
		self.reciptinent = reciptinent
		self.sender = sender
		self.time = time
		self.content = content
	def __repr__(self) :
		return f"<user: {self.content}>"
class notification() :
	def __init__(self, time, content, id, type) :
		self.time = time
		self.content = content
		self.id = id
		self.type = type
	def __repr__(self) :
		return f"<user: {self.content}>"
class user() :
	def __init__(self, username, email, password, gender) :
		self.username = username
		self.email = email
		self.password = password
		self.gender = gender
		self.messages = []
		self.friends=[]
		self.notifications=[]
		self.real = False
	def __repr__(self) :
		return f"<user: {self.username}>"
	def send_messege(self, other_part, content) :
		if self.real == True :
			messege=message(reciptinent=other_part,sender=self,time=datetime.now(),content=content)
			self.messages.append(messege)
			other_part.messages.append(messege)
	def delete(self) :
		if self.real == True :
			users.pop(self)
users = []
users.append(user(username="Yasin Mohammed", email="yasinmohammedbest@mail.com", password="Waslah", gender="male"))
users[0].real = True

@app.before_request
def before_request():
	g.user = None
	if 'user_Mail' in session:
		for user in users :
			if user.email == session['user_Mail'] :
				break
		g.user = user

@app.route('/')
def index() :
	return render_template('index.html')

@app.route('/profile')
def profile() :
	if not g.user :
		return redirect(url_for('login'))
	return render_template('profile.html',users=users)

@app.route("/signup", methods=["POST", "GET"])
def signup() :
	if request.method == "POST" :
		email = request.form['email']
		users.append(user(username = request.form['username'],email = email,password = request.form['password'], gender = request.form['gender']))
		session['user_Mail'] = email
		cocode = s.dumps(email, salt='email-confirm')
		msg = Message('Confirm Email', sender='Wasil@Waslah.com', recipients=[email])
		link = url_for('confirm_email', token=cocode, _external=True)
		msg.html = 'Your <em>link</em> is {}'.format(link)
		mail.send(msg)
		return render_template("notconfirmed.html")
	return render_template('signup.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		email = s.loads(token, salt='email-confirm', max_age=3600)
	except SignatureExpired:
		return render_template('expired.html')
	for user in users :
		if user.email == session['user_Mail'] :
			break
	user.real = True
	return redirect(url_for('profile'))

@app.route('/login', methods=["POST", "GET"])
def login() :
	if request.method == 'POST':
		session.pop('user_Mail', None)
		username = request.form['username']
		password = request.form['password']
		for user in users :
			if user.username == username :
				break
		if user and user.password == password:
			session['user_Mail'] = user.email
			return redirect(url_for('profile'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('user_Mail', None)
	return redirect(url_for('profile'))

@app.route('/sendmessage', methods=["POST"])
def sendmessage() :
	if not g.user :
		return redirect(url_for("profile"))
	if request.method == "POST" :
		other_part = request.form['reciptinent']
		if other_part == None :
			return redirect(url_for("profile"))
		for user in users :
			if user.username == other_part :
				other_part = user
				break
		content = request.form['content']
		g.user.send_messege(other_part, content)
		other_part.notifications.append(notification(time=datetime.now(), content="you have got a message", id=g.user.username+"!@!"+str(len(other_part.notifications))+"!@!"+other_part.username, type="message"))
	return redirect(url_for("profile"))

@app.route('/sendrequest', methods=["POST"])
def sendrequest() :
	if not g.user :
		return redirect(url_for("profile"))
	other_person = str(request.form['maybe'])
	if other_person == None :
		return redirect(url_for("profile"))
	for person in users :
		if person.username == other_person :
			other_person = person
			break
	other_person.notifications.append(notification(time=datetime.now(), content=g.user.username+" sent a friend request to you", id=g.user.username+"!@!"+str(len(other_person.notifications))+"!@!"+other_person.username, type="new friend"))
	return redirect(url_for("profile"))

@app.route('/done/<string:that_one>')
def seen(that_one) :
	content, sender, number, reciver = that_one.split("!@!")
	thati_one = sender + "!@!" + number + "!@!" + reciver
	for the_user in users :
		if the_user.username == sender :
			sender = the_user
			break
	for the_other_user in users :
		if the_other_user.username == reciver :
			reciver = the_other_user
			break
	for noti in reciver.notifications :
		if noti.id == thati_one :
			thati_one = noti
			break
	if thati_one.type == "message" :
		reciver.notifications.remove(thati_one)
		return redirect(url_for("profile"))
	if content == "yes" :
		sender.friends.append(reciver)
		reciver.friends.append(sender)
	reciver.notifications.remove(thati_one)
	return redirect(url_for("profile"))

'''#not arabic
languages = ["en"]
@app.route('/<string:lang>')
def langindex(lang) :
	if not(lang in languages) :
		return redirect(url_for('index'))
	return render_template(lang+'index.html')
@app.route('/profile/<string:lang>')
def langprofile(lang) :
	if not(lang in languages) :
		return redirect(url_for('profile'))
	if not g.user :
		return redirect(url_for('login/'+lang))
	return render_template(lang+'profile.html',users=users)

@app.route("/signup/<string:lang>", methods=["POST", "GET"])
def langsignup(lang) :
	if not(lang in languages) :
		return redirect(url_for('signup'))
	if request.method == "POST" :
		users.append(user(username = request.form['username'],email = request.form['email'],password = request.form['password'], gender = request.form['gender']))
		session['user_Mail'] = request.form['email']
		return redirect(url_for('profile/'+lang))
	return render_template(lang+'signup.html')

@app.route('/login/<string:lang>', methods=["POST", "GET"])
def langlogin(lang) :
	if not(lang in languages) :
		return redirect(url_for('login'))
	if request.method == 'POST':
		session.pop('user_Mail', None)
		username = request.form['username']
		password = request.form['password']
		for user in users :
			if user.username == username :
				break
		if user and user.password == password:
			session['user_Mail'] = user.email
			return redirect(url_for('profile/'+lang))
	return render_template(lang+'login.html')
@app.route('/logout/<string:lang>')
def langlogout(lang):
	if not(lang in languages) :
		return redirect(url_for('logout'))
	session.pop('user_Mail', None)
	return redirect(url_for('profile/'+lang))
@app.route('/sendmessage/<string:lang>', methods=["POST"])
def langsendmessage(lang) :
	if not(lang in languages) :
		return redirect(url_for('sendmessage'))
	if not g.user :
		return redirect(url_for("profile/"+lang))
	if request.method == "POST" :
		other_part = request.form['reciptinent']
		if other_part == None :
			return redirect(url_for("profile/"+lang))
		for user in users :
			if user.username == other_part :
				other_part = user
				break
		content = request.form['content']
		g.user.send_messege(other_part, content)
	return redirect(url_for("profile/"+lang))'''

@app.errorhandler(404)
def page_not_found(e):
	return render_template('notfound.html'), 404





if __name__ == "__main__":
	app.run()
