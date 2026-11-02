
from flask import request,render_template,redirect,url_for,Blueprint,flash,session


from werkzeug.security import generate_password_hash

from blueprintapp.app import db

# Modelo
from blueprintapp.usuarios.models import Usuario


bp_usuario = Blueprint('bp_usuario',__name__,template_folder='templates')


# LISTAR USUARIOS

@bp_usuario.route("/")
def index():

    usuarios = Usuario.query.all()

    return render_template('usuarios/index.html',usuarios=usuarios)


# CREAR USUARIO

@bp_usuario.route("/create", methods=['GET', 'POST'])
def create():

    if request.method == 'GET':

        return render_template('usuarios/create.html')

    elif request.method == 'POST':

        nombre = request.form.get('nombre')

        email = request.form.get('email')

        password = request.form.get('password')

        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:

            flash('El correo ya está registrado', 'danger')

            return redirect(url_for('bp_usuario.create'))

        password_hash = generate_password_hash(password)

        usuario = Usuario(nombre=nombre,email=email,password=password_hash)

        db.session.add(usuario)

        db.session.commit()

        flash('Usuario registrado correctamente', 'success')

        return redirect(url_for('bp_usuario.index'))


# EDITAR USUARIO

@bp_usuario.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'GET':

        return render_template('usuarios/edit.html',usuario=usuario)

    elif request.method == 'POST':

        usuario.nombre = request.form.get('nombre')

        usuario.email = request.form.get('email')

        password = request.form.get('password')

        if password:

            usuario.password = generate_password_hash(password)

        db.session.commit()

        flash('Usuario actualizado correctamente', 'success')

        return redirect(url_for('bp_usuario.index'))


# ELIMINAR USUARIO

@bp_usuario.route("/delete/<int:id>", methods=['POST'])
def delete(id):

    usuario = Usuario.query.get_or_404(id)

    # VERIFICAR SI EL USUARIO TIENE SESIÓN INICIADA
    if session.get('usuario_id') == usuario.id:

        flash('No se puede eliminar este usuario porque tiene una sesión iniciada.','danger')

        return redirect(url_for('bp_usuario.index'))

    # ELIMINAR USUARIO SI NO TIENE SESIÓN INICIADA
    db.session.delete(usuario)

    db.session.commit()

    flash('Usuario eliminado correctamente', 'success')

    return redirect(url_for('bp_usuario.index'))
