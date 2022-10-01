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
from models import db, User,Pokemones,Fav_Especie,Fav_Pokemones,Entrenador,Especie
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/pokemones",methods=["GET"])
def all_pokemon():
    all_pokemones = Pokemones.query.all()
    pokemones_serilized=[]
    for pokemon in all_pokemones:
        pokemones_serilized.append(pokemon.serialize())
    return jsonify(pokemones_serilized)

@app.route("/pokemones/<int:pokemon_id>",methods=["GET"])
def one_pokemon(pokemon_id):
    one=Pokemones.query.get(pokemon_id)
    return jsonify(one.serialize())

@app.route("/especies",methods=["GET"])
def all_especies():
    all_especies=Especie.query.all()
    especie_serialized=[]
    for especie in all_especies:
        especie_serialized.append(especie.serialize())
    return jsonify(especie_serialized)

@app.route("/especies/<int:especie_id>",methods=["GET"])
def one_especie(especie_id):
    one=Especie.query.get(especie_id)
    return jsonify(one.serialize())

@app.route("/entrenadores",methods=["GET"])
def all_entrenadores():
    all_entrenadores=Entrenador.query.all()
    entrenadores_serialized=[]
    for entrenador in all_entrenadores:
        entrenadores_serialized.append(entrenador.serialize())
    return jsonify(entrenadores_serialized)

@app.route("/entrenadores/<int:entrenadores_id>",methods=["GET"])
def one_entrenador(entrenadores_id):
    one=Entrenador.query.get(entrenadores_id)
    return jsonify(one.serialize())

@app.route("/users",methods=["GET"])
def all_users():
    all_user=User.query.all()
    user_serialized=[]
    for user in all_user:
        user_serialized.append(user.serialize())
    return jsonify(user_serialized)

@app.route("/users/favoritos",methods=["GET"]) 
def user_fav():
    all_favoritos=Fav_Especie.query.all()+Fav_Pokemones.query.all()
    favoritos_serialized=[]
    for fav in all_favoritos:
        favoritos_serialized.append(fav.serialize())
    return jsonify(favoritos_serialized)
    
@app.route("/favoritos/pokemons/<int:pokemones_id>",methods=["POST"]) 
def agregar_pokemon(pokemones_id):
    one=Pokemones.query.get(pokemones_id)
    user=User.query.get(1)
    if(one):
        new_fav=Fav_Pokemones()
        new_fav.email=user.email
        new_fav.pokemones_id=pokemones_id
        db.session.add(new_fav)
        db.session.commit()
        return "Agregado"
    else:
        raise APIException("No existe el pokemon",status_code=404)
    
@app.route("/favoritos/especie/<int:especie_id>",methods=["POST"]) 
def agregar_especie(especie_id):
    one=Especie.query.get(especie_id)
    user=User.query.get(1)
    if(one):
        new_fav=Fav_Especie()
        new_fav.email=user.email
        new_fav.especie_id=especie_id
        db.session.add(new_fav)
        db.session.commit()
        return "Especie agregada"
    else:
        raise APIException("No existe esa especie",status_code=404)
    
@app.route("/favoritos/pokemon/<int:pokemon_id>",methods=["DELETE"]) 
def eliminar_pokemon(pokemon_id):
    one=Fav_Pokemones.query.filter_by(pokemon_id=pokemon_id).first()
    if(one):
        db.session.delete(one)
        db.session.commit()
        return "Pokemon eliminado"
    else:
         raise APIException("No existe esa pokemon",status_code=404)
   

@app.route("/favoritos/especie/<int:especie_id>",methods=["DELETE"]) 
def eliminar_especie(especie_id):
    one=Fav_Especie.query.get(especie_id)
    if(one):
        db.session.delete(one)
        db.session.commit()
        return "Especie eliminada"
    else:
         raise APIException("No existe esa especie",status_code=404)



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
