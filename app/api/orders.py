from flask import request
from flask_restful import Resource

from app.flask_config import app
from utils.helpers import validate_keys, validate_list_keys
from utils.mq_tool import MQTool
from utils.orders.get import get_orders
from utils.orders.post import add_order
from utils.orders.put import update_order, get_order_by_id

order_created_evt = MQTool(queue_name="ORDER_CREATED")


class Orders(Resource):
    def get(self):
        data_list = get_orders()

        return {
                   "message": data_list
               }, 200

    def post(self):
        data_dict = request.get_json()

        validate_keys(json_data=data_dict, dict_keys={
            "user_id": {"type": int, "null": False},
            "products": {"type": list, "null": False},
        })

        validate_list_keys(
            keys_list=data_dict["products"], key_type=dict, key_name="dict")

        new_order = add_order(data_dict=data_dict)

        order_created_evt.mq_publish(dict_body={
            "transaction_id": str(new_order.transaction_id),
            "user_id": new_order.user_id,
            "products": new_order.products
        })

        return {
                   "id": str(new_order.id),
                   "transaction_id": str(new_order.transaction_id),
                   "message": "success"

               }, 201


@app.route("/api/orders/<order_id>", methods=["PUT"])
def put(order_id):
    data_dict = request.get_json()

    ok = update_order(order_id=order_id, data_dict=data_dict)

    if not ok:
        return {
            "message": "Order not found"
        }

    return {
               "message": "success"
           }, 200


@app.route("/api/orders/<order_id>", methods=["GET"])
def get(order_id):
    order = get_order_by_id(order_id)
    if order is None:
        return {
                   "message": "Order not found"
               }, 404
    payload = {
        "id": str(order.id),
        "transaction_id": order.transaction_id,
        "user_id": order.user_id,
        "products": order.products,
        "status": order.status,
        "error_msg": order.error_msg,
        "created_at": str(order.created_at),
        **({"total_price": order.total_price} if order.status == "processed" else {}),
        "updated_at": order.updated_at
    }

    payload = {k: v for k, v in payload.items() if v is not None}

    return payload, 200
