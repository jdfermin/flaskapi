from flask import Flask, current_app, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Directory(db.Model):
    __tablename__ = 'directory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def json(self):
        return{'id': id, 'name': self.name}

with app.app_context():
    db.create_all()

@app.route('/status/', methods = ['GET'])
def status():  # put application's code here
    return 'pong'

#crear directorio
@app.route('/directory/', methods = ['POST'])
def crear_directorio():
    try:
        data = request.get_json()
        new_directory = Directory(name = data['name'])
        db.session.add(new_directory)
        db.session.commit()
        return make_response(jsonify({'message': 'directorio creado'}),201)
    except:
        return make_response(jsonify({'message' : 'error creando directorio'}),400)

@app.route('/directory/', methods = ['GET'])
def get_directorios():
    try:
        directorios = Directory.query.all()
        return make_response(jsonify({'directorios' : [directorio.json() for directorio in directorios]}),200)
    except:
        return make_response(jsonify({'message' : 'error consultando directorios'}),500)

@app.route('/directory/<int:id>', methods = ['GET'])
def get_directorio(id):
    try:
        directorio = Directory.query.filter_by(id = id).first()
        return make_response(jsonify({'directorio': directorio.json()}),200)
    except:
        return make_response(jsonify({'message' : 'error consultando directorio'}),500)

@app.route('/directory/<int:id>', methods = ['PUT'])
def get_directorio(id):
    try:
        directorio = Directory.query.filter_by(id=id).first()
        if directorio:
            data = request.get_json()
            directorio.name = data['name']
            db.session.commit()
            return make_response(jsonify({'message' : 'directorio actualizado'}),200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except:
        return make_response(jsonify({'message' : 'error actualizando directorio'}),500)

@app.route('/directory/<int:id>', methods = ['DELETE'])
def get_directorio(id):
    try:
        directorio = Directory.query.filter_by(id=id).first()
        if directorio:
            db.session.delete(directorio)
            db.session.commit()
            return make_response(jsonify({'message' : 'directorio eliminado'}),200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except:
        return make_response(jsonify({'message' : 'error eliminando directorio'}),500)
