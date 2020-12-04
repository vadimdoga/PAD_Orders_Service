from app.api.orders import Orders
from app.flask_config import api, app
from utils.mq_tool import MQTool

import os
import threading

order_delivery_evt = MQTool(queue_name="ORDER_DELIVERY")
compensation_order_created_evt = MQTool(queue_name="COMPENSATION_ORDER_CREATED")

api.add_resource(Orders, '/api/orders', '/api/orders/<string:order_id>')

if __name__ == '__main__':
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))

    # start thread events
    final_order = threading.Thread(target=order_delivery_evt.mq_receive)
    compensate_order = threading.Thread(target=compensation_order_created_evt.mq_receive)

    final_order.start()
    compensate_order.start()

    app.run(debug=True, host=HOST, port=PORT)
