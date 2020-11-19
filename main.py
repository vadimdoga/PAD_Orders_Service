from app.api.orders import Orders
from app.flask_config import api, app

import os

base_path = os.getenv("BASE_PATH")

api.add_resource(Orders, base_path)

if __name__ == '__main__':
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    app.run(debug=True, host=HOST, port=PORT)
