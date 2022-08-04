from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


firebaseConfig = {
  'apiKey': "AIzaSyA5NXfd1fJ61NQtWKksugQKdzM997I7vQI",
  'authDomain': "karma-fdac3.firebaseapp.com",
  'projectId': "karma-fdac3",
  'storageBucket': "karma-fdac3.appspot.com",
  'messagingSenderId': "221816971691",
  'appId': "1:221816971691:web:19b8fae392b1d6a97e32ee",
  'measurementId': "G-99683MZDHS",
  'databaseURL': "https://karma-fdac3-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    error = ""
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user']= auth.create_user_with_email_and_password(email, password)
        user={'email':request.form['email'],
        'password':request.form['password'],
        'fullname':request.form['fullname'],
        'phone_number': request.form['phone_number']}
        db.child("Users").child(login_session['user']['localId']).set(user)


        return redirect(url_for('homett'))
        
    return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('homett'))

    else:
        return render_template("signin.html")
#Code goes above here
 
@app.route('/homett', methods=['GET', 'POST'])
def homett():
    if request.method=='POST':
        name = request.form['Name']
        number = request.form['People']


        user={'info': {'name':request.form['Name'],
        'number':request.form['People'],
        'datetime-local':request.form['date'],
        'text': request.form['Message']}}



        
        db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('reservation'))


    return render_template('homett.html')


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    hey = db.child("Users").child(login_session['user']['localId']).get().val()
    return render_template('reservation.html',hey=hey)

    

    



if __name__ == '__main__':
    app.run(debug=True)