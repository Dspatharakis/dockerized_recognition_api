#!/usr/bin/env python3
import os
import random
import sys
import time
import requests


def main():
    image = "./images/6.jpg" 
    a = requests.post("http://0.0.0.0:8000/", files={"file": open(image, "rb")})
    print(a)

if __name__ == "__main__":
    main()

