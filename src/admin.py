import os
from flask_admin import Admin
from models import db, User, Pokemones, Especie, Entrenador,Fav_Especie,Fav_Pokemones
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Pokemones, db.session))
    admin.add_view(ModelView(Especie, db.session))
    admin.add_view(ModelView(Entrenador, db.session))
    admin.add_view(ModelView(Fav_Especie, db.session))
    admin.add_view(ModelView(Fav_Pokemones, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))