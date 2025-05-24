from flask import Flask , redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#config 
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Admin site'
db=SQLAlchemy(app)

#----------Admin-----#
class Admin(db.Model):
    id= db.Column(db.INTEGER, nullable =False, primary_key= True, unique=True)
    username= db.Column(db.String, nullable= False, unique = True)
    password= db.Column(db.String, nullable=False)

#----------Roles--------------------#
class Role(db.Model):
    id= db.Column(db.Integer, nullable= False, primary_key= True,unique=True)
    role= db.Column(db.String, nullable= False, unique=True)
    acess_model= db.Column(db.String, nullable= False)
    time= db.Column(db.DateTime, default = datetime.utcnow)
    active= db.Column(db.Boolean, default=True)
    users=db.relationship('User', back_populates='role')

#----------------User-------------#
class User(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    firstname= db.Column(db.String(20), nullable= False, unique= True)
    lastname= db.Column(db.String(20), nullable= False, unique= True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    hash_password= db.Column(db.String(30), nullable= False)
    role_id= db.Column(db.Integer, db.ForeignKey('role.id'))
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    indicator= db.Column(db.Boolean, default=True)

    role= db.relationship('Role',back_populates='users' )

#------------------Routes-------#
@app.route('/')     
def home(): 
    return redirect(url_for('login_admin'))      

@app.route('/login_admin', methods=[ 'GET','POST'])
def login_admin():
    if request.method == 'POST':
      username= request.form.get('username').strip()
      password= request.form.get('password').strip()
      print(f'form: {username}')
      print(f'form: {password}')
      admin = Admin.query.filter_by(username = username, password = password).first()
      if admin:
          session['admin_id']= admin.id
          print(f'admin found: {admin.username}')
          return redirect(url_for('dashboard'))
      else:
          print('no admin found')
          return "Invalid user or password"
    return render_template('login.html')   
    
@app.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))
    return render_template('dashboard.html')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    roles = Role.query.all()      # ➡️ db nd get the all roles
    if request.method == 'POST':
      first= request.form.get('firstname')
      last= request.form.get('lastname')
      password= request.form.get('hash_password')    #case sensitive
      email= request.form.get('email')     
      default_role= Role.query.filter_by(role = 'User').first()   #User here is just a string

      if not default_role:
        return 'Default role user not found '          
    
      user= User(firstname= first, 
                  lastname=last, 
                  email=email, 
                  hash_password=password,
                  role_id= default_role.id)      #role_id= roleid
      db.session.add(user) 
      db.session.commit()
      return "User Added Successfully 🥳"
    return render_template('register.html')        

@app.route('/users')
def users():
    all_users= User.query.all()
    return render_template('users.html',users=all_users)      #users passing context var to jinja temp     #✔️

@app.route('/manage_user')
def manage_user():
    data = User.query.all()
    return render_template('manageuser.html', users=data)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user= User.query.get(user_id)
    if not user:
        return "User not found."
    if request.method == "POST":
        user.firstname= request.form.get('firstname')
        user.lastname= request.form.get('lastname')
        user.email= request.form.get('email')
        user.hash_password= request.form.get('hash_password') 

        db.session.commit()
        return redirect(url_for('manage_user'))
    return render_template('edit.html', user=user)

@app.route('/delete/<int:user_id>')
def delete(user_id):
        user = User.query.get(user_id)
        if not user:
            return "Unable to delete"
        db.session.delete(user)
        db.session.commit()
        print("User deleted")
        return redirect(url_for('manage_user'))
        
@app.route('/logout_user')
def logout_user():
    session.pop('admin_id',None)
    return redirect(url_for('login_admin'))

if __name__ =='__main__':
    with app.app_context():
            db.create_all()

            if not Role.query.filter_by(role ='User').first():
              default_role= Role(role='User', acess_model= 'basic_acess')
              db.session.add(default_role)
              db.session.commit()
    app.run(debug=True) 