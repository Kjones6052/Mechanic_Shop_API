# This file contains all the config setups

# Development Config
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True

# Testing Config
class TestingConfig:
    pass

# Production Config
class ProductionConfig:
    pass