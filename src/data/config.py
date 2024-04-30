from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')
#PAYMENTS_TOKEN = env('PAYMENTS_TOKEN')
SUPPORT_ID = env.int('SUPPORT_ID')
#MANAGER_ID = env.int('MANAGER_ID')

DB_USER = env('DB_USER')
DB_PASS = env('DB_PASS')
DB_HOST = env('DB_HOST')
DB_PORT = env('DB_PORT')
DB_NAME = env('DB_NAME')


def database_url_asyncpg(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME):
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


database_url = database_url_asyncpg(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
