from flask import Flask, render_template, url_for,request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import migrate, Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']= 'your_secret_key'
db= SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager= LoginManager(app)
login_manager.login_view= 'login'
login_manager.login_message_category='info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(20), nullable=True)
    email= db.Column(db.String(20),nullable= False)
    password= db.Column(db.String(80),nullable= False)

    def set_password(self,password):
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

@app.route('/',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email= request.form.get('email')
        password=request.form.get('password')
        user= User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user,remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash('login unsuccessful','danger')
    return render_template('login.html')
    
@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.name}!"





@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        name= request.form.get('name')
        email= request.form.get('email')
        password= request.form.get('password')
        hashed_password= generate_password_hash(password)
        new_user= User(name=name, email=email, password= hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

# @app.route('/submit',methods=['POST','GET'])
# def submit():
#     name = request.form.get('name')
#     email= request.form.get('email')
#     password= request.form.get('password')

#     if email!= '' and password!='' and name!='':
#         p=User(name=name,email=email, password=password)
#         db.session.add(p)
#         db.session.commit()

#     return f"Name: {name}, Email: {email}, Password: {password}"

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)