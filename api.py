import os
from dotenv import load_dotenv
from app_factory import create_app

# from werkzeug.contrib.fixers import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app)

# load env variables
load_dotenv()

# create flask app
app = create_app()


if __name__ == "__main__":
    print(os.environ["FLASK_RUN_HOST"])
    app.run(host=os.environ["FLASK_RUN_HOST"], port=os.environ["FLASK_RUN_PORT"])
