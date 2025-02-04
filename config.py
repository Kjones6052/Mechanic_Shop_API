# This file contains all the config setups

# Development Config
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:7Raffi!Codes7@localhost/mechanic_shop_db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"


# Testing Config
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'


# Production Config
class ProductionConfig:
    pass