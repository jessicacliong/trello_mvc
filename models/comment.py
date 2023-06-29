from init import db, ma
from marshmallow import fields

 # {id: 1, "message": "Comment 1", "user": {id: 1, name: "User 1"}, "card": {id: 1, title: "Card 1"}}
class Comment(db.Model): 
  __tablename__ = 'comments'

  id = db.Column(db.Integer, primary_key=True)
  message = db.Column(db.Text)
  # user_id is a foreign key, which connects to the Users table, id column
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)

  # Creating the relationship, using sqlalchemy
  #back_populates means it connects to user.py with comments and vice versa
  #define relationship    #Model    #Field of that model
  user = db.relationship('User', back_populates='comments') # {id: 1, name: "User 1"}
  card = db.relationship('Card', back_populates='comments')

#to handle serialization and deserialization
class CommentSchema(ma.Schema):
  user = fields.Nested('UserSchema', only=['name', 'email'])
  card = fields.Nested('CardSchema', exclude=['comments'])
#provide the fields
  class Meta:
    fields = ('id', 'message', 'card', 'user')
    ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)