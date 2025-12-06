from app import create_app
from app.config import config
import os


env = os.getenv('FLASK_ENV', 'development')
config_class = config.get(env, config['default'])

app = create_app(config_class)


if __name__ == '__main__':
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
