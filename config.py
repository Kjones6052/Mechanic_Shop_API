# This file contains all the config setups

# Development Config
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:7Raffi!Codes7@localhost/mechanic_shop_db'
    DEBUG = True

# Testing Config
class TestingConfig:
    pass

# Production Config
class ProductionConfig:
    pass