"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
import re
from flask import Flask, request, jsonify, url_for
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# Aqui se importan las clases del models.py
from models import db, User, Team, User_Team, Games, Favoritos, Postulacion, Registro
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_swagger import swagger
from utils import APIException, generate_sitemap
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from sqlalchemy import exc, update, and_, or_, not_
# Aqui se importan las clases del models.py


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
Migrate = Migrate(app, db)

Manager = Manager(app)
Manager.add_command("db", MigrateCommand)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Crear un usuario
# Los Roles seran los siguientes:
# El rol 1 será para el Administrador del sitio.
# El rol 2 será para el Jugador, por defecto todos los usuarios nuevos.
# El rol 3 será para el Manager del equipo.
@app.route("/signup", methods=["POST"])
def signup():
    # Regular expression that checks a valid email
    ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # Regular expression that checks a valid password
    preg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
    # Instancing the a new user
    user = User()
    # Checking email
    if (re.search(ereg, request.json.get("email"))):
        user.email = request.json.get("email")
    else:
        return "Invalid email format", 400
    # Checking password
    if (re.search(preg, request.json.get('password'))):
        pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
        user.password = pw_hash
    else:
        return "Invalid password format", 400
    # Aqui vamos a pedir username (nick), first and last name para crear la cuenta
    user.first_name = request.json.get("firstname")
    user.last_name = request.json.get("lastname")
    user.username = request.json.get("username")
    # Imagen y bio
    user.image = request.json.get("image")
    user.bio = request.json.get("bio")
    user.blizzardID = request.json.get("blizzardID")
    # Por defecto se le agrega el Rol #2
    user.role = "2"

    # Aqui se valida si el usuario & email ya estan en uso, si ambos ya estan, no permite crearlo nuevamente
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True}), 201
    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify("Error el usuario o correo ya existen en la DB!!"), 500


# Login del usuario
# Este endpoint va a recuperar la clave de la DB y validará si el password es correcto.
@app.route("/login", methods=["POST"])
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
            "user": user.serialize(),
            "msg": "success"
        }
        return jsonify(data), 200


# Listar todos los usuarios
@app.route('/user', methods=['GET'])
def get_all_users():
    users_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users_query))
    return jsonify(all_users), 200


# Listar usuario por nick
@app.route('/user', methods=['POST'])
def get_user():
    body = request.get_json()
    user = User.query.filter_by(username=body['username']).first()
    return jsonify(user.serialize()), 200

# Endpoint para editar el usuario
@app.route('/user/edit/<int:id_user>', methods=['PUT'])
def handle_user_update(id_user):
    # Regular expression that checks a valid email
    ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # Regular expression that checks a valid password
    preg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
    body = request.get_json()
    user1 = User.query.filter_by(ID=id_user).first()

    if user1 is None:
        raise APIException('User not found', status_code=404)
    if "firstname" in body:
        user1.first_name = body["firstname"]
    if "lastname" in body:
        user1.last_name = body["lastname"]
    if "email" in body:
        if (re.search(ereg, request.json.get("email"))):
            user1.email = request.json.get("email")
        else:
            return "Invalid email format", 400
    if "username " in body:
        user1.username = body["username"]
    if "password" in body:
        if (re.search(preg, request.json.get('password'))):
            pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
            user1.password = pw_hash
        else:
            return "Invalid password format", 400
    if "role" in body:
        user1.role = body["role"]
    if "bio" in body:
        user1.bio = body["bio"]
    if "image" in body:
        user1.image = body["image"]
    if "blizzardID" in body:        
        user1.blizzardID: body["blizzardID"]

    db.session.commit()

    return jsonify("Done"), 200


# Endpoint para crear y listar games
@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        games_query = Games.query.all()
        all_games = list(map(lambda x: x.serialize(), games_query))
        return jsonify(all_games), 200

    if request.method == 'POST':
        body = request.get_json()
        print(body.keys())
        games = Games.query.filter_by(ID=body['ID']).first()
        games.logo = body['logo']
        games.game = body['game']
        db.session.commit()

    return jsonify(games.serialize()), 201


# Endpoint para crear equipos con POST, con GET para traer la lista de equipos (TODOS) y con PUT para cambiar informacion del equipo dandola ID por el body
@app.route('/teams', methods=['GET', 'POST', 'PUT'])
def handle_team():
    if request.method == 'POST':
        body = request.get_json()
        team = Team(name=body['name'],
                    tag=body['tag'],
                    owner_ID=body['owner_ID'],
                    logo=body['logo'],
                    game_ID=body['game_ID']                    
                    )
        db.session.add(team)
        db.session.commit()
        return jsonify(team.serialize()), 200

    if request.method == 'GET':
        team_query = Team.query.all()
        list_team = list(map(lambda x: x.serialize(), team_query))
        return jsonify(list_team), 200

    if request.method == 'PUT':
        body = request.get_json()
        team = Team.query.filter_by(ID=body['team_ID']).first()
        print(team)
        print(team.logo)

        if team is None:
            raise APIException('Team not found', status_code=404)
        if "name" in body:
            team.name = body["name"]
        if "bio" in body:
            team.bio = body["bio"]
        if "logo" in body:
            team.logo = body["logo"]
        if "tag" in body:
            team.tag = body["tag"]
        if "owner_ID" in body:
            team.owner_ID = body["owner_ID"]

        db.session.commit()
        return jsonify("Team Updated"), 200


# Endpoint para listar un equipo en particular por ID
@app.route('/team/<int:team_ID>', methods=['GET'])
def getTeamInfo(team_ID):
    team_query = Team.query.filter_by(ID=team_ID)
    list_team = list(map(lambda x: x.serialize(), team_query))
    if not list_team:
        return jsonify("No existe el equipo"), 404
    return jsonify(list_team), 200

# Endpoint para listar team members de un equipo en particular
@app.route('/team/<int:team_ID>/list', methods=['GET'])
def getTeamMembers(team_ID):
    team_query = Team.query.filter_by(ID=team_ID).first()
    return jsonify(team_query.team_members()), 200


# Endpoint para crear una postulacion, la fecha debe venir como yyyy-mm-dd hh:mm:ss
@app.route('/postulacion/create', methods=['POST'])
def handle_postulacion():
    body = request.get_json()
    postulacion = Postulacion(
        start_date=body['start_date'], end_date=body['end_date'], team_ID=body['team_ID'], status='Abierta')
    db.session.add(postulacion)
    db.session.commit()
    return jsonify("Postulacion creada"), 200

# Endpoint para hacer un update sobre la postulacion
@app.route('/postulacion/<int:id_postulacion>', methods=['PUT'])
def update_postulacion(id_postulacion):
    body = request.get_json()
    postulacion = Postulacion.query.filter_by(ID=id_postulacion).first()
    if postulacion is None:
        raise APIException('Postulacion not found', status_code=404)
    if "end_date" in body:
        postulacion.end_date = body["end_date"]
    if "status" in body:
        postulacion.status = body["status"]

    db.session.commit()
    return jsonify("Postulacion actualizada"), 200

  
# Endpoint para listar todas las postulaciones por equipo
@app.route('/postulacion/<int:id_team>', methods=['GET'])
def getPostulacionbyTeam(id_team):
    body = request.get_json()
    postulacion = Postulacion.query.filter_by(team_ID=id_team)
    list_team = list(map(lambda x: x.serialize(), postulacion))
    return jsonify(list_team), 200

# Endpoint de registro, este se utiliza para que un usuario postule a un equipo
@app.route('/registro', methods=['POST'])
def handle_registro():
    if request.method == 'POST':
        body = request.get_json()
        reg = Registro(user_ID = body['user_ID'], postulacion_ID = body['postulacion_ID'], create_date = body['create_date'], status = "En Progreso")
        # post = Postulacion.query.filter_by(ID=body['ID']).first()
        # usr = User.query.filter_by(ID=body['IDUser']).first()
        # post.crear_post.append(usr)  

    try:
        db.session.add(reg)
        db.session.commit()
        return jsonify("Postulacion creada"), 200
    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify("El jugador ya tiene una postulacion activa"), 500


# Endpoint para hacer un update del registro
@app.route('/registro/update', methods=['POST'])
def handle_registro_update():
        body = request.get_json()
        reg = Registro.query.filter_by(ID=body['ID']).first()
        reg.status = body['status']                  
        db.session.commit()
        return jsonify("Registro Actualizado"), 200
   


# Endpoint para listar las postulaciones por ID
@app.route('/registro/<int:ID_post>/list', methods=['GET'])
def getPostulacion(ID_post):
    # post = Registro.query.get(postulacion_ID=ID)
    reg = Registro.query.filter_by(postulacion_ID=ID_post)
    list_team = list(map(lambda x: x.serialize(), reg))
    return jsonify(list_team), 200

   


# Endpoint de asignar players a equipos
@app.route('/team/reg', methods=['POST'])
def handle_teamMember():
    body = request.get_json()
    usr = User.query.filter_by(ID=body['user_ID']).first()
    team = Team.query.filter_by(ID=body['team_ID']).first()
    team.team_member.append(usr)

    try:
        db.session.commit()
        return jsonify(team.team_members()), 200
    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify("Error el jugador ya pertenece al equipo, no se puede agregar"), 500


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
    Manager.run()
