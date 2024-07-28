"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


            # ------ Acá empezamos -------

    # Traer todos los usuarios
@app.route('/users', methods=['GET']) 
def get_users():

    results_query = User.query.all()
    results = list(map(lambda item: item.serialize(), results_query))

    if results == []:
        return jsonify({"msg": "There are no users"}), 404
    
    response_body = {
        "results": results
    }
    return jsonify(response_body), 200

    # Traer todos los personajes
@app.route('/people', methods=['GET']) 
def get_characters():

    results_query = Character.query.all()
    results = list(map(lambda item: item.serialize(), results_query))

    if results == []:
        return jsonify({"msg": "There are no characters"}), 404

    response_body = {
        "results": results
    }
    return jsonify(response_body), 200

   # Traer todos los planetas
@app.route('/planets', methods=['GET']) 
def get_planets():

    results_query = Planet.query.all()
    results = list(map(lambda item: item.serialize(), results_query))

    if results == []:
        return jsonify({"msg": "There are no planets"}), 404

    response_body = {
        "results": results
    }
    return jsonify(response_body), 200

    # Traer un solo usuario
@app.route('/user/<int:id>', methods=['GET']) 
def get_a_user(id):

    result_query = User.query.filter_by(id=id).first()
    
    if result_query == None:
        return jsonify({"msg": "No user was found with that id"}), 404 
 
    response_body = {
        "result": result_query.serialize()
    }
    return jsonify(response_body), 200

    # Traer un solo personaje
@app.route('/people/<int:id>', methods=['GET']) 
def get_a_character(id):

    result_query = Character.query.filter_by(id=id).first()

    if result_query == []:
        return jsonify({"msg": "Not found"}), 404

    response_body = {
        "result": result_query.serialize()
    }
    return jsonify(response_body), 200

    # Traer un solo planeta
@app.route('/planets/<int:id>', methods=['GET']) 
def get_a_planet(id):

    result_query = Planet.query.filter_by(id=id).first()

    if result_query == []:
        return jsonify({"msg": "Not found"}), 404

    response_body = {
        "result": result_query.serialize()
    }
    return jsonify(response_body), 200

   # Listar todos los favoritos que pertenecen a un usuario
@app.route('/users/<int:id_user>/favorites', methods=['GET']) 
def get_favorites(id_user):

    results_query = Favorites.query.filter_by(id_user=id_user).all()
    results = list(map(lambda item: item.serialize(), results_query))

    if results == []:
        return jsonify({"msg": "This user has no favorite characters"}), 404

    response_body = {
        "results": results
    }
    return jsonify(response_body), 200

# Añadir planeta favorito al usuario actual
@app.route('/favorite/planet/<int:id_planet>', methods=['POST']) 
def add_favorite_planet(id_planet):

    data = request.json
    new_planet_favorite = Favorites(id_user=data["id_user"],id_planet=data["id_planet"])
    db.session.add(new_planet_favorite)
    db.session.commit()

    response_body = {
        "msg": "Planet successfully added to favorites",
    }
    return jsonify(response_body), 200

# Añadir personaje favorito a usuario
@app.route('/favorite/people/<int:id_character>', methods=['POST']) 
def add_favorite_character(id_character):

    data = request.json
    new_character_favorite = Favorites(id_user=data["id_user"],id_character=data["id_character"])
    db.session.add(new_character_favorite)
    db.session.commit()

    response_body = {
        "msg": "Character successfully added to favorites",
    }
    return jsonify(response_body), 200

    # Eliminar personaje favorito por su id
@app.route('/favorite/people/<int:id_character>', methods=['DELETE']) 
def delete_favorite_character(id_character):

    query_result = Favorites.query.filter_by(id=id_character).first()
    if query_result is None:
        return jsonify({"msg": "Character with this id not found in favorites"}), 404

    try:
        db.session.delete(query_result)
        db.session.commit()
        
        response_body = {
            "msg": "Character successfully deleted from favorites",
        }
        return jsonify(response_body), 200
    
    except:
        return jsonify({"msg": "An unexpected error occurred"}), 500

    # Eliminar planeta favorito por su id
@app.route('/favorite/planets/<int:id_planet>', methods=['DELETE']) 
def delete_favorite_planet(id_planet):
    query_result = Favorites.query.filter_by(id=id_planet).first()

    if query_result is None:
        return jsonify({"msg": "Planet with this id not found in favorites"}), 404

    try:
        db.session.delete(query_result)
        db.session.commit()
        
        response_body = {
            "msg": "Planet successfully deleted from favorites",
        }
        return jsonify(response_body), 200
    
    except:
        return jsonify({"msg": "An unexpected error occurred"}), 500

# this only runs if `$ python src/app.py` is executed ------> Esto no se modifica
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
