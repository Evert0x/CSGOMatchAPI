from decouple import config
APP_DEBUG = config('APP_DEBUG', cast=bool)
APP_HOST = config('APP_HOST')
APP_PORT = config('APP_PORT', cast=int)