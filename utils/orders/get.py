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
            # show error message only when status is failed
            **({"error_msg": order.error_msg} if order.status == "failed" else {}),
            **({"total_price": order.total_price} if order.status == "processed" else {}),
            "created_at": str(order.created_at),
            "updated_at": str(order.updated_at)
        })

    return data
