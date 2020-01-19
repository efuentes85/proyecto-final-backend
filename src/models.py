from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


User_Team = db.Table('user_team',
                     db.Column('user_ID', db.Integer, db.ForeignKey(
                         'user.ID'), primary_key=True),
                     db.Column('team_ID', db.Integer, db.ForeignKey(
                         'team.ID'), primary_key=True),
                     db.Column('isMember', db.String(50))
                     )

Favoritos = db.Table('favoritos',
                     db.Column('user_ID', db.Integer, db.ForeignKey(
                         'user.ID'), primary_key=True),
                     db.Column('games_ID', db.Integer, db.ForeignKey(
                         'games.ID'), primary_key=True)
                     )


class User(db.Model):
    __tablename__ = "user"
    ID = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer)
    bio = db.Column(db.Text)
    image = db.Column(db.String(200))
    blizzardID = db.Column(db.String(100))
    # user_reg = db.relationship("Postulacion", secondary=Registro, backref=db.backref(
    #     'crear_post', lazy='dynamic'))
    team_user = db.relationship(
        "Team", secondary=User_Team, backref=db.backref('team_member', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "id": self.ID,
            "role": self.role,
            "bio": self.bio,
            "image": self.image,
            "blizzardID": self.blizzardID


        }


class Postulacion(db.Model):
    __tablename__ = "postulacion"
    ID = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DATETIME)
    end_date = db.Column(db.DATETIME)
    status = db.Column(db.String(50))
    team_ID = db.Column(db.Integer, db.ForeignKey('team.ID'))
    # postulacion_reg = db.relationship('User', secondary=Registro, backref ='postulacion')
    # postulacion_reg = db.relationship(
    #     "User", secondary=Registro, backref=db.backref('user_reg', lazy='dynamic'))

    def serialize(self):
        return {
            "ID": self.ID,
            "team": self.team_ID,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date
        }


class Team(db.Model):
    __tablename__ = "team"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    bio = db.Column(db.Text)
    logo = db.Column(db.String(200))
    tag = db.Column(db.String(30))
    owner_ID = db.Column(db.Integer)
    game_ID = db.Column(db.Integer, db.ForeignKey('games.ID'))

    def serialize(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "tag": self.tag,
            "logo": self.logo,
            "owner": self.owner_ID,
            "bio": self.bio,
            "game_ID": self.game_ID
        }

    def team_members(self):
        return {
            "team_member": list(map(lambda x: x.serialize(), self.team_member))
        }


class Games(db.Model):
    __tablename__ = "games"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    logo = db.Column(db.String(100))
    # fav_user = db.relationship('User' , secondary = Favoritos , backref='games')
    fav_user = db.relationship(
        "User", secondary=Favoritos, backref=db.backref('fav_game', lazy='dynamic'))

    def serialize(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "logo": self.logo

        }


class Registro(db.Model):
    __tablename__ = "registro"
    ID = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    user_ID = db.Column(db.Integer, primary_key=True)
    postulacion_ID = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DATETIME, primary_key=True)
    status = db.Column(db.String(50))

    def serialize(self):
        return {
            "ID": self.ID,
            "user_ID": self.user_ID,
            "postulacion_ID": self.postulacion_ID,
            "create_date": self.create_date,
            "status": self.status

        }
