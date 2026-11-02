from flask import render_template,request,redirect,url_for,flash,session

from werkzeug.security import check_password_hash

from flask import Blueprint

from blueprintapp.usuarios.models import Usuario


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates')


# INICIAR SESION

@bp_auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('auth/login.html')

    elif request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password,password):

            session['usuario_id'] = usuario.id
            session['usuario'] = usuario.nombre

            flash('Bienvenido al sistema', 'success')

            return redirect(url_for('bp_core.index'))

        flash('Correo o contraseña incorrectos', 'danger')

        return redirect(url_for('bp_auth.login'))


# CERRAR SESION

@bp_auth.route("/logout")
def logout():

    session.clear()

    flash('Sesión cerrada correctamente', 'info')

    return redirect(url_for('bp_auth.login'))