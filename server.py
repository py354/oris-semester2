from server_module.handler import Server
import random
import time
import config

if __name__ == '__main__':
    random.seed(time.time())
    server = Server(config.SERVER_ADDRESS, config.DATABASE_FILE)
    server.run()
