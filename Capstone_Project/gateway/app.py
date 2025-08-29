from flask import Flask
from routes import gateway_routes
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(gateway_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
