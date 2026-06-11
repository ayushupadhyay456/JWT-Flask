from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_jwt_extended import create_access_token , JWTManager

app=Flask(__name__)

app.config['SECRET-KEY']='SUPER_SECRET-KEY'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db=SQLAlchemy(app)
api=Api(app)
jwt=JWTManager(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
with app.app_context():
    db.create_all()

class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']

        if not username or not password:
            return {'message':'Missing username or password'},400
        
        if User.query.filter_by(username=username).first():
            return {'message':'Ussrname already taken'},400
        
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message':'User Created Successfullly'},200

class UserLogin(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        user=User.query.filter_by(username=username).first()
        if user and user.password==password:
            access_token=create_access_token(identity=user.id)
            return  {'access_token':access_token}
        return  {'message':'Invalid_Credentials'},401
    
api.add_resource(UserRegistration,'/register')
api.add_resource(UserLogin,'/Login')

if __name__=='__main__':
    app.run(debug=True)