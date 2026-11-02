from blueprintapp.app import db


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String,nullable=False)

    email = db.Column(db.String,unique=True,nullable=False)

    password = db.Column(db.String,nullable=False)

    def __repr__(self):

        return f"<USUARIO {self.nombre} - {self.email}>"