from flask import Flask, jsonify, request

app = Flask(__name__)

class Request:
    def __init__(self, basket, zipCode, totalAmount):
        self.basket = basket
        self.zipCode = zipCode
        self.totalAmount = totalAmount

    def __str__(self):
        return 'basket:{}, zipCode:{}, totalAmount:{}'.format(self.basket, self.zipCode, self.totalAmount)

@app.route('/predict', methods=['POST'])
def predict():
    basket = request.json['basket']
    zipCode = request.json['zipCode']
    totalAmount = request.json['totalAmount']
    p = probability(Request(basket, zipCode, totalAmount))
    return jsonify({'probability': p}), 201

def probability(request):
    print("Processing request: {}".format(request))
    
    return 0.0

