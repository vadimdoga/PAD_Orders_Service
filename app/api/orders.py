from flask_restful import Resource
from flask import request

from utils.orders.post import add_order
from utils.orders.get import get_orders
from utils.orders.put import update_order
from utils.helpers import validate_keys, validate_list_keys
from utils.mq_tool import MQTool

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
            "message": "success"
        }, 201

    def put(self, order_id):
        data_dict = request.get_json()

        ok = update_order(order_id=order_id, data_dict=data_dict)

        if not ok:
            return {
                "error_msg": "Invalid order id"
            }

        return {
            "message": "success"
        }, 200
