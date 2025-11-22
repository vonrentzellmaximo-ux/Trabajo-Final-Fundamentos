from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petcare.db"
app.config["JWT_SECRET_KEY"] = "clave_secreta_segura"


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)




# MODELOS DE BASE DE DATOS
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(150), nullable=False)
   email = db.Column(db.String(150), unique=True, nullable=False)
   password = db.Column(db.String(150), nullable=False)


class Cliente(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(100), nullable=False)
   dni = db.Column(db.String(20), unique=True, nullable=False)
   email = db.Column(db.String(100))
   telefono = db.Column(db.String(50))


class Mascota(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(100), nullable=False)
   especie = db.Column(db.String(50))
   edad = db.Column(db.Integer)
   dueño_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)


class Turno(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   mascota_id = db.Column(db.Integer, db.ForeignKey("mascota.id"), nullable=False)
   veterinario = db.Column(db.String(100), nullable=False)
   fecha = db.Column(db.String(20))
   hora = db.Column(db.String(10))
   motivo = db.Column(db.String(200))


with app.app_context():
   db.create_all()




# AUTENTICACIÓN
@app.route("/register", methods=["POST"])
def register():
   data = request.get_json()
   nombre = data.get("nombre")
   email = data.get("email")
   password = data.get("password")


   if not nombre or not email or not password:
       return jsonify({"error": "Todos los campos son obligatorios"}), 400


   existente = User.query.filter_by(email=email).first()
   if existente:
       return jsonify({"error": "El email ya está registrado"}), 400


   hashed = bcrypt.generate_password_hash(password).decode("utf-8")
   nuevo = User(nombre=nombre, email=email, password=hashed)
   db.session.add(nuevo)
   db.session.commit()


   return jsonify({"mensaje": "Usuario registrado con éxito"}), 201




@app.route("/login", methods=["POST"])
def login():
   data = request.get_json()
   email = data.get("email")
   password = data.get("password")


   usuario = User.query.filter_by(email=email).first()


   if not usuario or not bcrypt.check_password_hash(usuario.password, password):
       return jsonify({"error": "Credenciales inválidas"}), 401


   token = create_access_token(identity=usuario.id)
   return jsonify({"token": token, "mensaje": "Inicio de sesión exitoso"})




# CRUD CLIENTES
@app.route("/clientes", methods=["GET"])
def obtener_clientes():
   clientes = Cliente.query.all()
   return jsonify([{"id": c.id, "nombre": c.nombre, "dni": c.dni, "email": c.email, "telefono": c.telefono} for c in clientes])


@app.route("/clientes", methods=["POST"])
def crear_cliente():
   data = request.get_json()
   nuevo = Cliente(nombre=data["nombre"], dni=data["dni"], email=data.get("email"), telefono=data.get("telefono"))
   db.session.add(nuevo)
   db.session.commit()
   return jsonify({"mensaje": "Cliente creado con éxito"}), 201


@app.route("/clientes/<int:id>", methods=["GET"])
def obtener_cliente(id):
   c = Cliente.query.get_or_404(id)
   return jsonify({"id": c.id, "nombre": c.nombre, "dni": c.dni, "email": c.email, "telefono": c.telefono})


@app.route("/clientes/<int:id>", methods=["PUT"])
def actualizar_cliente(id):
   c = Cliente.query.get_or_404(id)
   data = request.get_json()
   c.nombre = data.get("nombre", c.nombre)
   c.email = data.get("email", c.email)
   c.telefono = data.get("telefono", c.telefono)
   db.session.commit()
   return jsonify({"mensaje": "Cliente actualizado"})


@app.route("/clientes/<int:id>", methods=["DELETE"])
def eliminar_cliente(id):
   c = Cliente.query.get_or_404(id)
   db.session.delete(c)
   db.session.commit()
   return jsonify({"mensaje": "Cliente eliminado"})




# CRUD MASCOTAS
@app.route("/mascotas", methods=["GET"])
def obtener_mascotas():
   mascotas = Mascota.query.all()
   return jsonify([{"id": m.id, "nombre": m.nombre, "especie": m.especie, "edad": m.edad, "dueño_id": m.dueño_id} for m in mascotas])


@app.route("/mascotas", methods=["POST"])
def crear_mascota():
   data = request.get_json()
   nueva = Mascota(nombre=data["nombre"], especie=data["especie"], edad=data["edad"], dueño_id=data["dueño_id"])
   db.session.add(nueva)
   db.session.commit()
   return jsonify({"mensaje": "Mascota registrada"}), 201


@app.route("/mascotas/<int:id>", methods=["PUT"])
def actualizar_mascota(id):
   m = Mascota.query.get_or_404(id)
   data = request.get_json()
   m.nombre = data.get("nombre", m.nombre)
   m.edad = data.get("edad", m.edad)
   db.session.commit()
   return jsonify({"mensaje": "Mascota actualizada"})


@app.route("/mascotas/<int:id>", methods=["DELETE"])
def eliminar_mascota(id):
   m = Mascota.query.get_or_404(id)
   db.session.delete(m)
   db.session.commit()
   return jsonify({"mensaje": "Mascota eliminada"})




# CRUD TURNOS
@app.route("/turnos", methods=["GET"])
def obtener_turnos():
   turnos = Turno.query.all()
   return jsonify([{"id": t.id, "mascota_id": t.mascota_id, "veterinario": t.veterinario, "fecha": t.fecha, "hora": t.hora, "motivo": t.motivo} for t in turnos])


@app.route("/turnos", methods=["POST"])
def crear_turno():
   data = request.get_json()
   nuevo = Turno(
       mascota_id=data["mascota_id"],
       veterinario=data["veterinario"],
       fecha=data["fecha"],
       hora=data["hora"],
       motivo=data["motivo"]
   )
   db.session.add(nuevo)
   db.session.commit()
   return jsonify({"mensaje": "Turno registrado"}), 201


@app.route("/turnos/<int:id>", methods=["PUT"])
def actualizar_turno(id):
   t = Turno.query.get_or_404(id)
   data = request.get_json()
   t.fecha = data.get("fecha", t.fecha)
   t.hora = data.get("hora", t.hora)
   t.motivo = data.get("motivo", t.motivo)
   db.session.commit()
   return jsonify({"mensaje": "Turno actualizado"})


@app.route("/turnos/<int:id>", methods=["DELETE"])
def eliminar_turno(id):
   t = Turno.query.get_or_404(id)
   db.session.delete(t)
   db.session.commit()
   return jsonify({"mensaje": "Turno eliminado"})




# FILTROS EXTRA
@app.route("/turnos/mascota/<int:mascota_id>", methods=["GET"])
def turnos_por_mascota(mascota_id):
   turnos = Turno.query.filter_by(mascota_id=mascota_id).all()
   return jsonify([{"veterinario": t.veterinario, "fecha": t.fecha, "hora": t.hora, "motivo": t.motivo} for t in turnos])


@app.route("/turnos/veterinario/<nombre>", methods=["GET"])
def turnos_por_veterinario(nombre):
   turnos = Turno.query.filter(Turno.veterinario.like(f"%{nombre}%")).all()
   return jsonify([{"mascota_id": t.mascota_id, "fecha": t.fecha, "hora": t.hora, "motivo": t.motivo} for t in turnos])




# API EXTERNA (Gatos)
@app.route("/gatos/random", methods=["GET"])
def obtener_gato_random():
   respuesta = requests.get("https://api.thecatapi.com/v1/images/search")
   if respuesta.status_code == 200:
       return jsonify(respuesta.json())
   else:
       return jsonify({"error": "No se pudo obtener imagen de gato"}), 500




if __name__ == "__main__":
   app.run(debug=True)
