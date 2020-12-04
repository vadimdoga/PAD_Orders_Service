from models.orders import OrdersModel
from datetime import datetime
from utils.helpers import generate_uuid_key

import json
import logging


def add_order(data_dict):
    order = OrdersModel()

    order.transaction_id = generate_uuid_key()
    order.user_id = data_dict["user_id"]
    order.products = data_dict["products"]
    order.total_price = None
    order.status = "building"
    order.created_at = datetime.now()

    # pylint: disable=maybe-no-member
    new_order = OrdersModel.objects.insert(order)

    return new_order


def update_final_order(data_body):
    data_dict = json.loads(data_body)

    # pylint: disable=maybe-no-member
    order = OrdersModel.objects(transaction_id=data_dict["transaction_id"]).first()
    if order == None:
        logging.info("Invalid transaction_id")
        return False

    OrdersModel.update(order,
        status="delivered",
        updated_at=datetime.now(),
        products=data_dict["products"],
        total_price=data_dict["total_price"]
    )

    return True
