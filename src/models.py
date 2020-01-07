from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


User_Team = db.Table('user_team',
    db.Column('user_ID', db.Integer, db.ForeignKey('user.ID'), primary_key=True),
    db.Column('team_ID', db.Integer, db.ForeignKey('team.ID'), primary_key=True),
    db.Column('isMember', db.String(50))
)

Favoritos = db.Table('favoritos', 
    db.Column('user_ID', db.Integer, db.ForeignKey('user.ID'), primary_key=True),
    db.Column('games_ID', db.Integer, db.ForeignKey('games.ID'), primary_key=True)
)

Registro = db.Table('registro',
    db.Column('user_ID', db.Integer, db.ForeignKey('user.ID'), primary_key=True),
    db.Column('postulacion_ID', db.Integer, db.ForeignKey('postulacion.ID'), primary_key=True),
    db.Column('status', db.String(50))
)

class User(db.Model):
    __tablename__="user"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100)) 
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer)
    bio = db.Column(db.Text)
    image = db.Column(db.String(200))
    user_team = db.relationship("Team", secondary = User_Team , backref= 'user')
    user_fav = db.relationship("Games", secondary = Favoritos , backref= 'user')
    user_reg = db.relationship("Postulacion", secondary = Registro , backref= 'user')


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "firstname": self.first_name,
            "email": self.email,
            "id": self.ID,
            "role": self.role

        }

class Team(db.Model):
    __tablename__="team"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    bio = db.Column(db.Text)
    logo = db.Column(db.String(200))
    tag = db.Column(db.String(30))
    owner_ID = db.Column(db.Integer)
    game_ID = db.Column(db.Integer, db.ForeignKey('games.ID'))
    team_user = db.relationship('User', secondary = User_Team, backref='team')

    
    def serialize(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "tag": self.tag,
            "logo": self.logo,
            "owner": self.owner_ID                      
        }        

class Games(db.Model):
    __tablename__="games"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    logo = db.Column(db.String(100))
    fav_user = db.relationship('User' , secondary = Favoritos , backref='games')

    
    def serialize(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "logo": self.logo
                      
        }

class Postulacion(db.Model):
    __tablename__="postulacion"
    ID = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DATETIME)
    end_date = db.Column(db.DATETIME)
    status = db.Column(db.String(50))
    team_ID = db.Column(db.Integer, db.ForeignKey('team.ID'))
    postulacion_reg = db.relationship('User', secondary=Registro, backref ='postulacion')

    
    def serialize(self):
        return {
            "ID": self.ID,
            "team": self.team_ID,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date                      
        }



# class Registro(db.Model):
#     __tablename__="registro"
#     ID_user = db.Column(db.Integer,db.ForeignKey('User.ID') , primary_key=True)
#     ID_postulacion = db.Column(db.Integer, db.ForeignKey('Postulacion.ID'), primary_key = True)
#     status = db.Column(db.String(50))
    
#     def serialize(self):
#         return {
#             "ID_user": self.ID_user,
#             "ID_postulacion": self.ID_postulacion,
#             "status": self.status                             
#         }

