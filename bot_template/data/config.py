from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')
SUPPORT_ID = env.int('SUPPORT_ID')