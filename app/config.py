import os


class Config:
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    CRAWLER_TIMEOUT = int(os.getenv('CRAWLER_TIMEOUT', 10))
    CRAWLER_MAX_PAGES = int(os.getenv('CRAWLER_MAX_PAGES', 100))
    CRAWLER_DELAY = float(os.getenv('CRAWLER_DELAY', 0.1))
    CRAWLER_USER_AGENT = os.getenv('CRAWLER_USER_AGENT', 'Mozilla/5.0 (DFS Web Crawler)')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
