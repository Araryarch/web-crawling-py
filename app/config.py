import os


class Config:
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Crawler basic config
    CRAWLER_TIMEOUT = int(os.getenv('CRAWLER_TIMEOUT', 10))
    CRAWLER_MAX_PAGES = int(os.getenv('CRAWLER_MAX_PAGES', 100))
    CRAWLER_MAX_DEPTH = int(os.getenv('CRAWLER_MAX_DEPTH', 10))
    CRAWLER_DELAY = float(os.getenv('CRAWLER_DELAY', 0.1))
    CRAWLER_USER_AGENT = os.getenv('CRAWLER_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Crawler bypass config
    CRAWLER_VERIFY_SSL = os.getenv('CRAWLER_VERIFY_SSL', 'False') == 'True'
    CRAWLER_RETRY_COUNT = int(os.getenv('CRAWLER_RETRY_COUNT', 3))
    CRAWLER_RETRY_DELAY = float(os.getenv('CRAWLER_RETRY_DELAY', 1.0))
    CRAWLER_FOLLOW_REDIRECTS = os.getenv('CRAWLER_FOLLOW_REDIRECTS', 'True') == 'True'
    CRAWLER_ROTATE_USER_AGENT = os.getenv('CRAWLER_ROTATE_USER_AGENT', 'True') == 'True'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
