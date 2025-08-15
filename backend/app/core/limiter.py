from slowapi import Limiter
from slowapi.util import get_remote_address


# Single limiter instance shared across the app
limiter = Limiter(key_func=get_remote_address)


