from init import db, ma
from marshmallow import fields

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  is_admin = db.Column(db.Boolean, default=False)

                          #Model   #field of that model #as per designed in ERD cards
  cards = db.relationship('Card', back_populates='user', cascade='all, delete')
                              #Model   #field of that model  #as per ERD cards
  comments = db.Relationship('Comment', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
  cards = fields.List(fields.Nested('CardSchema', exclude=['user']))
  comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))
  # exclude = the schema doesn't include that field
  #here its done to prevent recursion, user calls cards which calls user which calls cards ...
  class Meta:
    fields = ('id', 'name', 'email', 'password', 'is_admin', 'cards', 'comments')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])