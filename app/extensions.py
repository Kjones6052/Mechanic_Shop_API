# This file is for incorporating extensions

# Imports
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Instantiate
ma = Marshmallow()
limiter = Limiter(key_func=get_remote_address, 
                  default_limits=["200/day", "50/hour"])

cache = Cache()