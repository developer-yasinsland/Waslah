from flask import Flask, render_template, request, g, session, redirect, url_for, flash
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = "KytaRsmbineL2"
class message() :
    def __init__(self, reciptinent, sender, time, content) :
        self.reciptinent = reciptinent
        self.sender = sender
        self.time = time
        self.content = content
    def __repr__(self) :
        return f"<user: {self.content}>"
class user() :
    def __init__(self, username, email, password, gender) :
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.messages = []
    def __repr__(self) :
        return f"<user: {self.username}>"
    def send_messege(self, other_part, content) :
        messege=message(reciptinent=other_part,sender=self,time=datetime.now(),content=content)
        self.messages.append(messege)
        other_part.messages.append(messege)
    def delete(self) :
        self = None
users = []
users.append(user(username="Yasin Mohammed", email="yasinmohammedbest@gmail.com", password="Waslah", gender="male"))


@app.before_request
def before_request():
    g.user = None
    if 'user_Mail' in session:
        for user in users :
            if user.email == session['user_Mail'] :
                break
        g.user = user

@app.route('/')
def profile() :
    if not g.user :
        return redirect(url_for('login'))
    return render_template('profile.html',users=users)

@app.route("/signup", methods=["POST", "GET"])
def signup() :
    if request.method == "POST" :
        users.append(user(username = request.form['username'],email = request.form['email'],password = request.form['password'], gender = request.form['gender']))
        session['user_Mail'] = request.form['email']
        return redirect(url_for('profile'))
    return render_template('signup.html')

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
    return redirect(url_for("profile"))








if __name__ == "__main__":
    app.run()