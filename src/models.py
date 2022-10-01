from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Pokemones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    ataque = db.Column(db.String(30), unique=False, nullable=False)
    defensa = db.Column(db.String(30), unique=False, nullable=False)
    evoluciones = db.Column(db.String(30), unique=False, nullable=False)
    imagen = db.Column(db.String(30), unique=False, nullable=False)
    rel_name = db.relationship('Entrenador', backref='pokemones', lazy=True)
    
    def __repr__(self):
        return '<Pokemones %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "ataque":self.ataque,
            "defensa":self.defensa,
            "evoluciones":self.evoluciones,
            "imagen":self.imagen,
            # do not serialize the password, its a security breach
        }
class Especie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(30), unique=True, nullable=False)
    habilidades = db.Column(db.String(30), unique=False, nullable=False)
    
    
    def __repr__(self):
        return '<Especie %r>' % self.especie

    def serialize(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "habilidades":self.habilidades
            # do not serialize the password, its a security breach
        }

class Fav_Pokemones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemones_id = db.Column(db.Integer, db.ForeignKey('pokemones.id') )
    email =  db.Column(db.String(120), db.ForeignKey('user.email'))
    rel_name = db.relationship('Pokemones')
    rel_user = db.relationship('User')


    def __repr__(self):
        return '<Fav_people %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "pokemones_id": self.pokemones_id,
            "email": self.email
            # do not serialize the password, its a security breach
        }
class Fav_Especie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String(120), db.ForeignKey('user.email'))
    Especie_especie=db.Column(db.String(30),db.ForeignKey('especie.especie'))
    rel_user = db.relationship('User')
    rel_especie=db.relationship('Especie')

    def __repr__(self):
        return '<Fav_people %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "especie":self.Especie_especie,
            "email": self.email
            # do not serialize the password, its a security breach
        }
class Entrenador(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=False, nullable=False)
    pokemon_principal=db.Column(db.Integer,db.ForeignKey('pokemones.id'))
    


    def __repr__(self):
        return '<Fav_people %r>' % self.name

    def serialize(self):
            return{
                "id":self.id,
                "name":self.name,
                "pokemon_principal":self.pokemones.name
            }
