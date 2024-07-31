from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    birth_year = db.Column(db.String(120), unique=False, nullable=True)
    height = db.Column(db.String(120), unique=False, nullable=True)
    eye_color = db.Column(db.String(120), unique=False, nullable=True)
    skin_color = db.Column(db.String(120), unique=False, nullable=True)
    hair_color = db.Column(db.String(120), unique=False, nullable=True)
    favorite_character = db.relationship("Favorites", backref="character", lazy=True)


    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        print(self.favorite_character)
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
        }
    

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(120), unique=False, nullable=True)
    terrain = db.Column(db.String(120), unique=False, nullable=True)
    climate = db.Column(db.String(120), unique=False, nullable=True)
    orbital_period = db.Column(db.String(120), unique=False, nullable=True)
    rotation_period = db.Column(db.String(120), unique=False, nullable=True)
    diameter = db.Column(db.String(120), unique=False, nullable=True)
    favorite_planet = db.relationship("Favorites", backref="planet", lazy=True)


    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id_character = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=True)
    id_planet = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        query_user = User.query.filter_by(id=self.id_user).first()
        query_character = Character.query.filter_by(id=self.id_character).first()
        query_planet = Planet.query.filter_by(id=self.id_planet).first()
         
        return {
            "id": self.id,
            "user": query_user.serialize(),
            "character": query_character.serialize()["name"] if query_character else None,
            "planet": query_planet.serialize()["name"] if query_planet else None
        }
    