import json
import logging
from datetime import datetime

from models.orders import OrdersModel
from utils.helpers import generate_uuid_key


def add_order(data_dict):
    order = OrdersModel()
    order.transaction_id = generate_uuid_key()
    order.user_id = data_dict["user_id"]
    order.products = data_dict["products"]
    order.total_price = None
    order.status = "building"
    order.created_at = datetime.now()
    logging.info(f"Start Order processing", extra={"transaction_id": order.transaction_id})

    # pylint: disable=maybe-no-member
    new_order = OrdersModel.objects.insert(order)

    return new_order


def update_final_order(data_body, q_name):
    data_dict = json.loads(data_body)
    # pylint: disable=maybe-no-member

    order = OrdersModel.objects(transaction_id=data_dict["transaction_id"]).first()
    if order is None:
        logging.error("Order with such transaction_id doesn't exist",
                      extra={"transaction_id": data_dict["transaction_id"]})
        return False
    if q_name == "ORDER_DELIVERY":
        logging.info(f"Order Ready for Delivery", extra={"transaction_id": data_dict["transaction_id"]})
        OrdersModel.update(order,
                           status="processed",
                           updated_at=datetime.now(),
                           products=data_dict["products"],
                           total_price=data_dict["total_price"]
                           )
    elif q_name == "COMPENSATION_ORDER_CREATED":
        logging.info(f"Order Failed", extra={"transaction_id": data_dict["transaction_id"]})
        OrdersModel.update(order,
                           status="failed",
                           updated_at=datetime.now(),
                           error_msg=data_dict["error_msg"]
                           )
