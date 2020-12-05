from mongoengine import StringField, DateTimeField, ListField, IntField, ObjectIdField, FloatField, Document
from bson.objectid import ObjectId


class OrdersModel(Document):
    transaction_id = StringField(required=True)
    user_id = IntField(required=True)
    products = ListField(required=True)
    status = StringField(required=True)
    error_msg = StringField()
    total_price = FloatField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField()
