from flask import Flask, jsonify, request
import pickle
import pandas as pd
app = Flask(__name__)

with open('model.pck','rb') as f:
    logreg_up= pickle.load(f)
print(logreg_up)

class Request:
    def __init__(self, basket, zipCode, totalAmount):
        self.basket = basket
        self.zipCode = zipCode
        self.totalAmount = totalAmount

    def __str__(self):
        return 'basket:{}, zipCode:{}, totalAmount:{}'.format(self.basket, self.zipCode, self.totalAmount)

@app.route('/predict', methods=['POST'])
def predict():
    
    print('INSIDE predict')
    
    
    basket = request.json['basket']
    zipCode = request.json['zipCode']
    totalAmount = request.json['totalAmount']
    
    print(basket, zipCode, totalAmount)
    
    pd.DataFrame([basket, zipCode, totalAmount])
    
    # Transform the     
    
    df['c_0'] = df.basket.map(lambda x: x.count(0))
    df['c_1'] = df.basket.map(lambda x: x.count(1))
    df['c_2'] = df.basket.map(lambda x: x.count(2))
    df['c_3'] = df.basket.map(lambda x: x.count(3))
    df['c_4'] = df.basket.map(lambda x: x.count(4))
    
    dummies = pd.get_dummies(df.zipCode)
    
    
    p = probability(Request(basket, zipCode, totalAmount))
    
    print('Returning', jsonify({'probability': p}))
    
    return jsonify({'probability': p}), 201

def probability(request):
    print("Processing request: {}".format(request))
    
    return 0.0

