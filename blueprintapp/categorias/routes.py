# Librerías
from flask import request,render_template,redirect,url_for,Blueprint,flash


# Base de datos
from blueprintapp.app import db

# Modelo
from blueprintapp.categorias.models import Categoria

from blueprintapp.anuncios.models import Anuncio


bp_categoria = Blueprint('bp_categoria',__name__,template_folder='templates')


# LISTAR CATEGORIAS

@bp_categoria.route("/")
def index():

    categorias = Categoria.query.all()

    return render_template('categorias/index.html', categorias=categorias)


# CREAR CATEGORIA

@bp_categoria.route("/create", methods=['GET', 'POST'])
def create():

    if request.method == 'GET':

        return render_template('categorias/create.html')

    elif request.method == 'POST':

        nombre = request.form.get('nombre')

        descripcion = request.form.get('descripcion')

        categoria_existente = Categoria.query.filter_by(nombre=nombre).first()

        if categoria_existente:

            flash('La categoría ya existe', 'danger')

            return redirect(url_for('bp_categoria.create'))

        categoria = Categoria( nombre=nombre, descripcion=descripcion)

        db.session.add(categoria)

        db.session.commit()

        flash('Categoría registrada correctamente', 'success')

        return redirect(url_for('bp_categoria.index'))


# EDITAR CATEGORIA

@bp_categoria.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):

    categoria = Categoria.query.get_or_404(id)

    if request.method == 'GET':

        return render_template('categorias/edit.html',categoria=categoria)

    elif request.method == 'POST':

        categoria.nombre = request.form.get('nombre')

        categoria.descripcion = request.form.get('descripcion')

        db.session.commit()

        flash('Categoría actualizada correctamente', 'success')

        return redirect(url_for('bp_categoria.index'))


# ELIMINAR CATEGORIA
@bp_categoria.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    categoria = Categoria.query.get_or_404(id)

    anuncios_asociados = Anuncio.query.filter_by(categoria_id=categoria.id).count()

    if anuncios_asociados > 0:
        flash(f'No se puede eliminar la categoría "{categoria.nombre}" 'f'porque tiene {anuncios_asociados} anuncio(s) publicado(s).','danger')
        return redirect(url_for('bp_categoria.index'))

    db.session.delete(categoria)
    db.session.commit()

    flash('Categoría eliminada correctamente.', 'success')
    return redirect(url_for('bp_categoria.index'))