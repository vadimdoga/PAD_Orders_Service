from models.orders import OrdersModel
from datetime import datetime


def get_order_by_id(order_id):
    order = OrdersModel.objects(id=order_id).first_or_404()

    return order


def update_order(order_id, data_dict):
    order = get_order_by_id(order_id=order_id)

    OrdersModel.update(order, status=data_dict["new_status"], updated_at=datetime.now())
