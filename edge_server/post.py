#!/usr/bin/env python3
from  multiprocessing import dummy
import os
import random
import sys
import time
import requests

IP_ADDR = os.getenv('EDGE_SERVER_IP_ADDR')
if IP_ADDR is None:
    sys.exit("Environmemnt variable 'EDGE_SERVER_IP_ADDR' is not set")

PORT = os.getenv('EDGE_SERVER_PORT')
if PORT is None:
    sys.exit("Environmemnt variable 'EDGE_SERVER_PORT' is not set")

POST_URL = "http://%s:%s/" % (IP_ADDR, PORT)

IMAGES_PATH = os.getenv('IMAGES_PATH', '/tmp/images/')

IMAGES = []
for (dirpath, dirnames, filenames) in os.walk(IMAGES_PATH):
    IMAGES.extend(filenames)
    break
print('Discovered images: {}'.format(IMAGES))

def post_once():
    image = os.path.join(IMAGES_PATH, random.choice(IMAGES))
    print('Using image: {}'.format(image))
    try:
        requests.post(POST_URL, files={"file": open(image, "rb")})
    except requests.exceptions.ConnectionError as err:
        print('Error while trying to post once: {}'.format(err))

DURATION = float(os.getenv('DURATION', '60.0'))
REQUESTS_PER_30 = float(os.getenv('REQUESTS_PER_30', '5.0'))
POOL = dummy.Pool(16)

def main():
    start_time = time.time()
    while (time.time() - start_time) < DURATION:
        time.sleep(random.expovariate(REQUESTS_PER_30 / 30.0))
        POOL.apply_async(post_once)

if __name__ == "__main__":
    main()
