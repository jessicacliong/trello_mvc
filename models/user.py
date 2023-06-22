from init import db, ma

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
  cards = fields.List(fields.Nested('CardSchema', exclude=['user']))
  #exclude = the schema doesn't include that field
  #here its done to prevent recursion, user calls cards which calls user which calls cards ...

  class Meta:
    fields = ('id', 'name', 'email', 'password', 'is_admin')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])