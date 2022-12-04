from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import raw_data
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:" #БД хранится не в проекте, а в памяти, можно указать db_test.db

db = SQLAlchemy(app) #Связали БД с приложением

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }
'''User model created'''


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }
'''Order model created'''


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }
'''Offer model created'''

#---------------------------Views-------------------------

@app.route("/users", methods = ['GET', 'POST'])
def users():
    if request.method == "GET":
        result = []
        for user in User.query.all():
            result.append(user.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)

        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

        return "User created", 201

@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def user(uid: int):
    if request.method == 'GET':
        return json.dumps(User.query.get(uid).to_dict()), 200
    if request.method == 'PUT':
        user_data = json.loads(request.data)
        user = User.query.get(uid)
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.age = user_data["age"]
        user.email = user_data["email"]
        user.role = user_data["role"]
        user.phone = user_data["phone"]

        db.session.add(user)
        db.session.commit()

        return 'User updated', 204

    if request.method == 'DELETE':
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()

        return 'User deleted', 204

#-------------------Orders views------------------
@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        result = []
        for order in Order.query.all():
            result.append(order.to_dict())

        return json.dumps(result), 200

    if request.method == 'POST':
        order_data = json.loads(request.data)
        new_order = Order(
        id=order_data["id"],
        name = order_data["name"],
        description = order_data["description"],
        start_date = order_data["start_date"],
        end_date = order_data["end_date"],
        address = order_data["address"],
        price = order_data["price"],
        customer_id = order_data["customer_id"],
        executor_id = order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

        return 'Order created', 201

@app.route('/order/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def order(uid: int):
    if request.method == 'GET':
        return json.dumps(Order.query.get(uid).to_dict()), 200

    if request.method == 'PUT':
        order_data = json.loads(request.data)
        order = Order.query.get(uid)
        order.name = order_data["name"]
        order.description = order_data["description"]
        order.start_date = order_data["start_date"],
        order.end_date = order_data["end_date"],
        order.address = order_data["address"],
        order.price = order_data["price"],
        order.customer_id = order_data["customer_id"],
        order.executor_id = order_data["executor_id"]

        db.session.add(order)
        db.session.commit()

        return "Order updated", 204

    if request.method == 'DELETE':
        order = Order.query.get(uid)

        db.session.delete(order)
        db.session.commit()

        return "Order deleted", 204

#------------------Offer views-------------------
@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        result = []
        for offer in Offer.query.all():
            result.append(offer.to_dict())

        return json.dumps(result), 200

    if request.method == 'POST':
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            customer_id=offer_data["customer_id"],
            executor_id=offer_data["executor_id"]
        )
        db.session.add(new_offer)
        db.session.commit()

        return 'Offer created', 201

@app.route('/offer/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def offer(uid: int):
    if request.method == 'GET':
        return json.dumps(Offer.query.get(uid).to_dict()), 200

    if request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = Offer.query.get(uid)
        offer.id = offer_data["id"]
        offer.customer_id = offer_data["customer_id"]
        offer.executor_id = offer_data["executor_id"],

        db.session.add(offer)
        db.session.commit()

        return "Offer updated", 204

    if request.method == 'DELETE':
        offer = Offer.query.get(uid)

        db.session.delete(offer)
        db.session.commit()


#-------------------init database-----------------
def init_database():
    db.drop_all()
    db.create_all()
    '''Clear database, create database'''

    for user_data in raw_data.users:
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()
    '''Add users to database'''

    for order_data in raw_data.orders:
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["email"],
            address=order_data["role"],
            price=order_data["phone"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()
    '''Add order to order table'''

    for offer_data in raw_data.offers:
        new_offer = Offer(
            id=offer_data["id"],
            customer_id=offer_data["customer_id"],
            executor_id=offer_data["executor_id"]
        )

        db.session.add(new_offer)
        db.session.commit()
    '''Add offers to offer table'''

if __name__ == '__main__':
    init_database()
    app.run(debug=True)