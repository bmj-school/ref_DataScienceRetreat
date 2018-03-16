#!/usr/bin/env python

import random, math
import json, os

print("Generating test data", end='', flush=True)
os.makedirs("data/fraud-data", exist_ok=True)


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

def totalAmount(fraud, itemsInBasket):
	if(fraud):
		return itemsInBasket*max((int)(random.gauss(70, 30)),10)
	else:
		return itemsInBasket*max((int)(random.gauss(50, 30)),10)

def jsonLine():
	fraud = random.randint(0, 100) < 3
	basketItems = basket(fraud)
	return json.dumps({
		"customerID": customerId(),
		"basket": basketItems,
		"zipCode": zipCode(fraud),
		"totalAmount": totalAmount(fraud, len(basketItems)),
		"fraudLabel": 1 if(fraud) else 0
		})

def createLog(day):
	textFile = open("data/fraud-data/"+day+".txt", 'w')
	for i in range(0, 1000):
		textFile.write(jsonLine() + "\n")
	textFile.close()

for i in range(1,32):
	print(".",end='', flush=True)
	createLog("2017-01-{0:02d}".format(i))
print("done!")
