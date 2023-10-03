import json


from munch import DefaultMunch
from flask import Flask, request, jsonify
from src.calculate_application import calculate_output


app = Flask(__name__)


@app.route('/customer', methods=['POST'])
def calculate_customer():
    """
    Calculate for one customer
    """
    # Get input from request
    customer_data = json.loads(request.data)

    # Convert json to object Application
    application = DefaultMunch.fromDict(customer_data)

    return jsonify(calculate_output(application))


@app.route('/customers', methods=['POST'])
def calculate_customers():
    """
    Calculate for multiple customers
    """

    # Get input from request
    customers_data = json.loads(request.data)

    # Response
    response = []

    for customer in customers_data:
        # Convert json to object Application
        application = DefaultMunch.fromDict(customer)
        response.append(calculate_output(application))

    return jsonify(response)


if __name__ == '__main__':
    app.run()
