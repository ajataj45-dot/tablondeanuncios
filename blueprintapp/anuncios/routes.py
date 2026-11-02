from flask import request,render_template,redirect,url_for,Blueprint,flash,session

from blueprintapp.app import db

from blueprintapp.anuncios.models import Anuncio
from blueprintapp.usuarios.models import Usuario
from blueprintapp.categorias.models import Categoria


bp_anuncio = Blueprint('bp_anuncio',__name__,template_folder='templates')


# LISTAR ANUNCIOS
@bp_anuncio.route("/")
def index():

    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).all()
    return render_template('anuncios/index.html',anuncios=anuncios)


# CREAR ANUNCIO
@bp_anuncio.route("/create", methods=['GET', 'POST'])
def create():

    if not session.get('usuario_id'):
        flash('Debes iniciar sesión para publicar un anuncio', 'warning')
        return redirect(url_for('bp_auth.login'))

    if request.method == 'GET':

        categorias = Categoria.query.all()

        return render_template('anuncios/create.html',categorias=categorias)

    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    ubicacion = request.form.get('ubicacion')
    contacto = request.form.get('contacto')
    categoria_id = request.form.get('categoria_id')

    if not titulo or not descripcion or not ubicacion or not contacto or not categoria_id:
        flash('Completa todos los campos', 'danger')
        return redirect(url_for('bp_anuncio.create'))

    categoria = Categoria.query.get_or_404(categoria_id)

    anuncio = Anuncio(titulo=titulo,descripcion=descripcion,ubicacion=ubicacion,contacto=contacto,usuario_id=session['usuario_id'],categoria_id=categoria.id)

    db.session.add(anuncio)
    db.session.commit()

    flash('Anuncio publicado correctamente', 'success')

    return redirect(url_for('bp_anuncio.index'))


# EDITAR ANUNCIO
@bp_anuncio.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):

    anuncio = Anuncio.query.get_or_404(id)

    if not session.get('usuario_id'):
        flash('Debes iniciar sesión', 'warning')
        return redirect(url_for('bp_auth.login'))

    if anuncio.usuario_id != session['usuario_id']:
        flash('No puedes editar un anuncio de otro usuario', 'danger')
        return redirect(url_for('bp_anuncio.index'))

    categorias = Categoria.query.all()

    if request.method == 'GET':

        return render_template('anuncios/edit.html',anuncio=anuncio,categorias=categorias)

    anuncio.titulo = request.form.get('titulo')
    anuncio.descripcion = request.form.get('descripcion')
    anuncio.ubicacion = request.form.get('ubicacion')
    anuncio.contacto = request.form.get('contacto')

    categoria_id = request.form.get('categoria_id')

    categoria = Categoria.query.get_or_404(categoria_id)
    anuncio.categoria_id = categoria.id

    db.session.commit()

    flash('Anuncio actualizado correctamente', 'success')

    return redirect(url_for('bp_anuncio.index'))


# ELIMINAR ANUNCIO
@bp_anuncio.route("/delete/<int:id>", methods=['POST'])
def delete(id):

    anuncio = Anuncio.query.get_or_404(id)

    if not session.get('usuario_id'):
        flash('Debes iniciar sesión', 'warning')
        return redirect(url_for('bp_auth.login'))

    if anuncio.usuario_id != session['usuario_id']:
        flash('No puedes eliminar un anuncio de otro usuario', 'danger')
        return redirect(url_for('bp_anuncio.index'))

    db.session.delete(anuncio)
    db.session.commit()

    flash('Anuncio eliminado correctamente', 'success')

    return redirect(url_for('bp_anuncio.index'))