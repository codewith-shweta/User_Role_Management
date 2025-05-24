from app import db ,Admin   
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)          #imp when u create db obj outside the file and to bind db to current file

with app.app_context():
    db.create_all()

    if not Admin.query.filter_by(username='admin').first():
        host = Admin(username= 'sidd', password= "sidd1234")
        db.session.add(host)
        db.session.commit()
        print ("Admin created")
    else:
        print("Admin fail to create")


# with app.app_context():
#     db.create_all()

#     if not Admin.query.filter_by(username ='admin').first():
#         host = Admin(username='localhost', password='localhost890')
#         db.session.add(host)
#         db.session.commit()
#         print("Admin is created!")
#     else:
#         print("Admin fail to create")
