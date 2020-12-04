from models.orders import OrdersModel


def get_orders():
    data = []
    all_orders = OrdersModel.objects.all()

    for order in all_orders:
        data.append({
            "id": str(order.id),
            "transaction_id": order.transaction_id,
            "user_id": order.user_id,
            "products": order.products,
            "status": order.status,
            "created_at": str(order.created_at),
            "updated_at": str(order.updated_at)
        })

    return data
