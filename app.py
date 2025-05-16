from flask import Flask
from application.database import *
import datetime

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master_v1.sqlite3'
    db.init_app(app)
    app.app_context().push()
    with app.app_context():
        from application import models
        db.create_all()
        create_default_admin()
    return app

def create_default_admin():
    from application.models import User
    
    admin_user = User.query.filter_by(type='admin').first()
    
    if not admin_user:
        admin_user = User(
            username='admin',
            password='admin',
            full_name='Administrator',
            qualification='System Administrator',
            date_of_birth=datetime.date(2000, 1, 1),
            type='admin'
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print('Default admin user created')
    else:
        print('Admin user already exists')



app = create_app()
from application.controllers import *

if __name__ == '__main__':
    app.run()
