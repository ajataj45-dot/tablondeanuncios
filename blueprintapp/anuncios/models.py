from blueprintapp.app import db


class Anuncio(db.Model):

    __tablename__ = "anuncios"

    id = db.Column(db.Integer,primary_key=True)

    titulo = db.Column(db.String,nullable=False)

    descripcion = db.Column(db.String,nullable=False)

    ubicacion = db.Column(db.String,nullable=False)

    contacto = db.Column(db.String,nullable=False)

    fecha_publicacion = db.Column(db.DateTime,server_default=db.func.now())

    usuario_id = db.Column(db.Integer,db.ForeignKey('usuarios.id'),nullable=False)

    categoria_id = db.Column(db.Integer,db.ForeignKey('categorias.id'),nullable=False)

    usuario = db.relationship('Usuario',backref='anuncios')

    categoria = db.relationship('Categoria',backref='anuncios')

    def __repr__(self):
        return f'<ANUNCIO {self.titulo}>'



