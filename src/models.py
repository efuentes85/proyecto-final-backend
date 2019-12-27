from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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


    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "id": self.ID,
            "role": self.role

        }


class Games(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    logo = db.Column(db.String(100))

    
    def serialize(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "logo": self.logo
                      
        }
