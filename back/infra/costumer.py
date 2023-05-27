import json
import requests
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app) 

db = SQLAlchemy(app)




# Customers model
class Customers(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    age = db.Column(db.String(100))

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'age': self.age,
        }


# Function to display customers
@app.route('/show-customers', methods=['GET'])
def show_customers():
    customers_list = [customer.to_dict() for customer in Customers.query.all()]
    return jsonify(customers_list)


# Function to add a customer
@app.route('/add-customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data.get('name')
    city = data.get('city')
    age = data.get('age')

    new_customer = Customers(name, city, age)
    db.session.add(new_customer)
    db.session.commit()
    return "A new record was created."


# Function to delete a customer
@app.route('/delete-customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customers.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return 'Customer deleted.'
    else:
        return 'Customer not found.'