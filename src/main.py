"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
import re
from flask import Flask, request, jsonify, url_for
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, User
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_swagger import swagger

from utils import APIException, generate_sitemap
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from sqlalchemy import exc
#Aqui se importan las clases del models.py
from models import db, User, Games

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = "secret-key"
app.config['JWT_SECRET_KEY'] = 'encrypt'
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)
Migrate = Migrate(app,db)

Manager = Manager(app)
Manager.add_command("db" , MigrateCommand)



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#Crear un usuario
#Los Roles seran los siguientes:
#El rol 1 será para el Administrador del sitio.
#El rol 2 será para el Jugador, por defecto todos los usuarios nuevos.
#El rol 3 será para el Manager del equipo.
@app.route("/signup", methods=["POST"])
def signup():
        #Regular expression that checks a valid email
        ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        #Regular expression that checks a valid password
        preg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        # Instancing the a new user
        user = User()
        #Checking email 
        if (re.search(ereg,request.json.get("email"))):
            user.email = request.json.get("email")
        else:
            return "Invalid email format", 400
        #Checking password
        if (re.search(preg,request.json.get('password'))):
            pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
            user.password = pw_hash
        else:
            return "Invalid password format", 400
        #Aqui vamos a pedir username (nick), first and last name para crear la cuenta
        user.firstname = request.json.get("firstname")
        user.lastname = request.json.get("lastname")
        user.username = request.json.get("username")  
        user.role = "2"      

         #Aqui se valida si el usuario & email ya estan en uso, si ambos ya estan, no permite crearlo nuevamente
        try:
            db.session.add(user)  
            db.session.commit()
            return jsonify({"success": True}), 201 
        except exc.IntegrityError as e:     
            db.session().rollback()      
            return jsonify("Error el usuario o correo ya existen en la DB!!"), 500


        

#Login del usuario
#Este endpoint va a recuperar la clave de la DB y validará si el password es correcto.
@app.route("/login",methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Email not found"}), 404
    
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        data = {
            "access_token": access_token,
            "user" : user.serialize(),
            "msg": "success"
        }
        return jsonify(data), 200



#Listar todos los usuarios
@app.route('/user', methods=['GET'])
def get_all_users():
    users_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users_query))
    return jsonify(all_users), 200



# @app.route('/signup', methods=['POST'])
# def create_user():
#     body = request.get_json()
#     user1 = User(username=body['username'],
#                 first_name=body['first_name'] ,
#                 last_name=body['last_name'] ,
#                  email=body['email'],
#                  role='2')
#     db.session.add(user1)
#     db.session.commit()
#     return jsonify(user1.serialize()), 200




@app.route('/game', methods=['GET'])
def show_games():
    games_query = Games.query.all()
    all_games = list(map(lambda x: x.serialize(), games_query))
    return jsonify(all_games), 200


@app.route('/game', methods=['POST'])
def create_game():
    body = request.get_json()
    print(body.keys())   
    game = Games(name=body['game'],
                    logo=body['logo'])
    db.session.add(game)
    db.session.commit()

    return jsonify(game.serialize()), 201

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
    Manager.run()