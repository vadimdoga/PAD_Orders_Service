from models.orders import OrdersModel
from datetime import datetime
import logging


def get_order_by_id(order_id):
    # pylint: disable=maybe-no-member
    order = OrdersModel.objects(id=order_id).first()

    return order


def update_order(order_id, data_dict):
    order = get_order_by_id(order_id=order_id)
    if order == None:
        logging.info("Invalid order_id")
        return False

    OrdersModel.update(order, status=data_dict["new_status"], updated_at=datetime.now())

    return True
