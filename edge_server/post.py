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

#POST_URL = "http://%s:%s/" % (IP_ADDR, PORT)

POST_URL = "http://edge-server-cv.default.svc.cluster.local:8000/"


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
        a = requests.post(POST_URL, files={"file": open(image, "rb")})
    except requests.exceptions.ConnectionError as err:
        print('Error while trying to post once: {}'.format(err))
    print(a, file=open("output.txt", "a"))

DURATION = float(os.getenv('DURATION', '3600.0'))
REQUESTS_PER_30 = float(os.getenv('REQUESTS_PER_30', '5.0'))
POOL = dummy.Pool(16)


def main():
    start_time = time.time()
    rate = 75 
    total_counter =0 
    interval = 1 
    while (time.time() - start_time) < DURATION:
        rate +=1
        counter = 0
        while (time.time() - start_time) < 30 * interval:
            sleep_time = random.expovariate(rate / 30.0)
            if (time.time() + sleep_time - start_time >= 30* interval): 
                time.sleep(30*interval - time.time() + start_time )
                break
            time.sleep(sleep_time)
            POOL.apply_async(post_once)
            counter +=1

        print ("interval", interval)
        print ("rate", rate)
        print ("counter", counter)
        print ("time", time.time() - start_time)
        interval += 1
        counter = 0 
if __name__ == "__main__": 
    main()
