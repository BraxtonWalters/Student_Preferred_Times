from flask_app import app
#! import controllers 
from flask_app.controllers import controller_route, controller_user, controller_time




if __name__ == "__main__":
    app.run(debug=True)