import random
import sys
import time

import redis
import requests


def send_presence():
    while True:
        nonce = random.randint(1, 100000)
        redis_cli = redis.Redis()
        port = sys.argv[-1]
        username = redis_cli.get(f"gharar_username_{port}")
        requests.post(f'http://localhost:8080/presence?nonce={nonce}', data={'username': username, 'port': port})
        time.sleep(1)
