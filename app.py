from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView 
from flask_login import UserMixin,LoginManager,login_user,logout_user,current_user

app=Flask(__name__)
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SECRET_KEY']='c6e910dd901f0e6ebf307fd3511dc165f3b10a0d9e0f717933a85a3f5f18eba0'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
login_manager=LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(100))
    def __repr__(self):
        return f"User('{self.name}','{self.email}')"

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('home'))
 
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

admin=Admin(app,index_view=MyAdminIndexView())
admin.add_view(MyModelView(User,db.session))

@app.route('/home')
def home():
    return '<h1>This is my homepage.</h1>'

@app.route('/login/<int:my_id>')
def login(my_id):
    user=User.query.get(my_id)
    login_user(user)
    return '<h1>You are logged in</h1>'

@app.route('/logout')
def logout():
    logout_user()
    return '<h1>You logged out ,you can loggin again</h1>'


if __name__=='__main__':
    app.run(debug=True)