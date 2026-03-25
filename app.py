from flask import Flask
from controllers.auth_controller import auth_blueprint

app = Flask(__name__)
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
    