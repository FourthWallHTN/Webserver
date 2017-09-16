from flask import Flask, render_template
import unirest, json, uuid

# Cockroach DB imports
from __future__ import print_function
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

################
### API Keys ###
################

square_application_id = 'sandbox-sq0idp-NMjTA4x9HyDSGNWXdwc2Pg'
square_access_token = 'sandbox-sq0atb-VGm6YqbVmufgp9MHE3j1FQ'

################
### Database ###
################

def initDB():
	# Create database
	Base = declarative_base()

	# The Account class corresponds to the "accounts" database table.
	class Account(Base):
	    __tablename__ = 'accounts'
	    id = Column(Integer, primary_key=True)
	    balance = Column(Integer)
	    card_nonce = Column(Integer)

	# The Items class corresponds to the "items" database table.
	class Item(Base):
	    __tablename__ = 'items'
	    id = Column(Integer, primary_key=True)
	    count = Column(Integer)
	    sold = Column(Integer)
	    price = Column(Float)

	# Create an engine to communicate with the database. The "cockroachdb://" prefix
	# for the engine URL indicates that we are connecting to CockroachDB.
	engine = create_engine("cockroachdb://maxroach@localhost:26257/bank?sslmode=disable")
	Session = sessionmaker(bind=engine)

	# Automatically create the "accounts" and "items" tables based on the Account and Item classes.
	Base.metadata.create_all(engine)

	# Insert two rows into the "accounts" table.
	session = Session()
	session.add_all([
	    Account(id=1, balance=1000, card_nonce = ),
	    Account(id=2, balance=250, card_nonce = ),
	])
	session.commit()

##############
### Routes ###
##############

# Display seller dashboard with statistics
@app.route('/')
@app.route('/seller')
def seller():
	return render_template("dashboard.html")

# Display buyer page to connect accounts for Coinbase and Square, see history/info/etc
@app.route('/buyer')
def buyer():
	pass

# Execute payment through Square API
@app.route('/pay/square/<int:item_id>', methods=['GET','POST'])
def square(item_id):

	# Sandbox Location ID (Coffee & Toffee NYC)
	location_id = 'CBASEEKdEq0dwQd9aigzQlUVGhYgAQ'
	card_nonce = 'FAKE_CARD_NONCE'

	response = unirest.post('https://connect.squareup.com/v2/locations/' + location_id + '/transactions',
		headers={
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + square_access_token,
		},
		params = json.dumps({
			'card_nonce': card_nonce,
			'amount_money': {
				'amount': 100,
				'currency': 'USD'
			},
			'idempotency_key': str(uuid.uuid1())
		})
	)

	return json.dumps(response.body)

# Generate card nonce for Square payment
def newCardNonce():
	pass

# Execute payment through Coinbase API
@app.route('/pay/coinbase/<int:item_id>', methods=['GET','POST'])
def coinbase(item_id):
	pass

if __name__ == "__main__":
	app.debug = True
	app.run('0.0.0.0', port=8000)