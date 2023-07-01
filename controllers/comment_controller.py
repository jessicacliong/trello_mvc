from flask import Blueprint
from flask import Blueprint, request
from init import db
from models.card import Card
from models.comment import Comment, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__)

# /cards/card_id/comments - POST

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(card_id):
    body_data = request.get_json()
    stmt = db.select(Card).filter_by(id=card_id) #select * from cards where id= card_id
    card = db.session.scalar(stmt)
    if card:
        comment = Comment(
            message=body_data.get('message'),
            user_id=get_jwt_identity(), #pass id to the _id field
            card = card #card_id=card.id #pass the model instance to the model field
        )

        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    else:
        return {'error' : f'Card not found with id (card_id)'}, 404

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(card_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'message': f'Comment {comment.message} deleted successfully'}
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404

@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(card_id, comment_id):
    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt) #comment from database that needs to be updated
    if comment:
        comment.message = body_data.get('message') or comment.message #if body_data.get('message') is True, its passed as the value, if false but comment.message is true, comment.message value gets passed. Boolean logic 
        # comment.message = body_data.get('message') also works here
        db.session.commit()
        return comment_schema.dump(comment)
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404


#command+shft+l to highlight the routes and edit them simultaneously 