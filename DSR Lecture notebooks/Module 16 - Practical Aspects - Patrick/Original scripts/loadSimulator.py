#!/usr/bin/env python

import random, math
import json, os
import requests
import time

fraudZip = [random.randint(math.pow(10, 4), math.pow(10, 5)) for i in range(0, 1000)]
def zipCode(fraud):
	if(fraud):
		return fraudZip[random.randint(0, 1000-2)]
	else:
		return random.randint(math.pow(10, 4), math.pow(10, 5))

def customerId():
	return random.randint(math.pow(10,9), math.pow(10, 10))

def fraudCategory():
	rand = random.randint(0, 10)
	if(rand > 5):
		return 4
	if(rand > 2):
		return 3
	return rand

def basket(fraud):
	size = max((int)(random.gauss(5, 3)),1)
	if(fraud):
		return [fraudCategory() for i in range(0, size)]
	else:
		return [random.randint(0, 4) for i in range(0, size)]

def totalAmount(fraud, itemsInBasket, i):
	factor = 1 if i < 2000 else 10
	if(fraud):
		return itemsInBasket*max((int)(random.gauss(70, 30)),10)/factor
	else:
		return itemsInBasket*max((int)(random.gauss(50, 30)),10)/factor

def jsonLine(i):
	fraud = random.randint(0, 100) < 3
	basketItems = basket(fraud)
	return json.dumps({
		"customerID": customerId(),
		"basket": basketItems if random.randint(0, 10) > 1 else None,
		"zipCode": zipCode(fraud) if random.randint(0, 10) > 1 else None,
		"totalAmount": totalAmount(fraud, len(basketItems), i) if random.randint(0, 10) > 1 else None
		})

for i in range(1, 10000):
	print("Sending request...")
	headers = {'content-type': 'application/json'}
	r = requests.post("http://localhost:5000/predict", data=jsonLine(i), headers=headers)
	print("Received answer: " + str(r.text))
	time.sleep(1)

print("done!")
