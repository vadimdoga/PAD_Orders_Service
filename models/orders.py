from mongoengine import StringField, DateTimeField, ListField, IntField, ObjectIdField, FloatField
from bson.objectid import ObjectId
from app.flask_config import db

class OrdersModel(db.Document):
    transaction_id = StringField(required=True)
    user_id = IntField(required=True)
    products = ListField(required=True)
    status = StringField(required=True)
    total_price = FloatField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField()
