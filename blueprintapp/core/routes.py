from flask import render_template, Blueprint

from blueprintapp.anuncios.models import Anuncio
from blueprintapp.usuarios.models import Usuario
from blueprintapp.categorias.models import Categoria


bp_core = Blueprint('bp_core',__name__,template_folder='templates')


@bp_core.route("/")
def index():

    total_anuncios = Anuncio.query.count()
    total_usuarios = Usuario.query.count()
    total_categorias = Categoria.query.count()

    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).limit(5).all()

    return render_template('core/index.html',total_anuncios=total_anuncios,total_usuarios=total_usuarios,total_categorias=total_categorias,anuncios=anuncios)
    