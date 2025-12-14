from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.domain.entities import CrawlConfig
from app.container.service_container import init_container


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object(config_class)
    
    with app.app_context():
        crawl_config = CrawlConfig(
            timeout=app.config['CRAWLER_TIMEOUT'],
            max_pages=app.config['CRAWLER_MAX_PAGES'],
            max_depth=app.config['CRAWLER_MAX_DEPTH'],
            delay=app.config['CRAWLER_DELAY'],
            user_agent=app.config['CRAWLER_USER_AGENT'],
            verify_ssl=app.config['CRAWLER_VERIFY_SSL'],
            retry_count=app.config['CRAWLER_RETRY_COUNT'],
            retry_delay=app.config['CRAWLER_RETRY_DELAY'],
            follow_redirects=app.config['CRAWLER_FOLLOW_REDIRECTS'],
            rotate_user_agent=app.config['CRAWLER_ROTATE_USER_AGENT']
        )
        init_container(crawl_config)
    
    from app.presentation.routes import bp
    app.register_blueprint(bp)
    
    return app
