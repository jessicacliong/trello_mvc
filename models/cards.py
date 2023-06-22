from init import db, ma

class Card(db.Model):
  __tablename__ = "cards"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db. String(100))
  description = db.Column(db.Text)
  date = db.Column(db.Date) # Date created
  status = db.Column(db.String, nullable=False)
  priority = db.Column(db.String)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  user = db.relationship('User', back_populates='cards')
  # user: { value of the user id card to be created} creates the relationship the card with the user

class CardSchema(ma.Schema):
  user = fields.Nested('UserSchema', only=['name', 'email']) 

  class Meta:
    fields = ('id', 'title', 'description', 'date', 'status', 'priority', 'user')
    ordered = True

card_schema = CardSchema()
cards_schema = CardSchema(many=True)
