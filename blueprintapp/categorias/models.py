from blueprintapp.app import db


class Categoria(db.Model):

    __tablename__ = "categorias"

    id = db.Column(db.Integer,primary_key=True)

    nombre = db.Column(db.String,nullable=False,unique=True)

    descripcion = db.Column(db.String,nullable=False)

    def __repr__(self):

        return f"<CATEGORIA {self.nombre}>"