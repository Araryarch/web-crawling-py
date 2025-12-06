from flask import Flask
from app.config import Config
from app.domain.entities import CrawlConfig
from app.container.service_container import init_container


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    with app.app_context():
        crawl_config = CrawlConfig(
            timeout=app.config['CRAWLER_TIMEOUT'],
            max_pages=app.config['CRAWLER_MAX_PAGES'],
            delay=app.config['CRAWLER_DELAY'],
            user_agent=app.config['CRAWLER_USER_AGENT']
        )
        init_container(crawl_config)
    
    from app.presentation.routes import bp
    app.register_blueprint(bp)
    
    return app
