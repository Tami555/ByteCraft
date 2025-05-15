import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Users'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    FirstName = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    LastName = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='-')
    Password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    PhoneNumber = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Image_Avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    IdCard = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Bonus_Cards.Id'), default=0)
    card = orm.relationship('Card')
    favorites = orm.relationship("Product", secondary="Favorites", backref="users", lazy='dynamic')

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)
    
    def get_id(self):
        return self.Id