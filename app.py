from __future__ import print_function
from flask import Flask, render_template
import unirest, json, uuid

# SQLAlchemy imports
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
	    #balance = Column(Integer)
	    card = Column(Integer)

	# The Items class corresponds to the "items" database table.
	class Item(Base):
	    __tablename__ = 'items'
	    id = Column(Integer, primary_key=True)
	    name = Column(String)
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
	    Account(id=1, card=4532759734545858 ),	# Visa
	    Account(id=2, card=5409889944179029),	# MasterCard
	    Account(id=3, card=6011033621379697),	# Discover
	    Account(id=4, card=36004244846408),		# Diners Club
	    Account(id=5, card=3566005734880650),	# JCB
	    Account(id=6, card=371263462726550),	# American Express
	    Account(id=7, card=6222520119138184),	# China UnionPay
	    Item(id=1, name="Chair", count=20, sold=0, price=39.99),
	    Item(id=2, name="Table", count=10, sold=0, price=89.99),
	    Item(id=3, name="Lamp", count=10, sold=0, price=25.99),
	])
	session.commit()

##############
### Routes ###
##############

# Display seller dashboard with statistics
@app.route('/')
@app.route('/seller')
def seller():
	# revenue = calculateRevenue()

	return render_template("dashboard.html")

# def calculateRevenue():
# 	revenue = 0
	
# 	return revenue

# Display buyer page to connect accounts for Coinbase and Square, see history/info/etc
@app.route('/buyer')
def buyer():
	return render_template("paymentForm.html", application_id = square_application_id, postal_code="94103",expiration_date="04/20",card_number="4532759734545858",cvv="111")

# Display item info
@app.route('/item/<int:item_id>')
def display_item_info(item_id):
	#item_name = Item.query() # (SELECT name FROM items WHERE id = item_id);
	item_price = "$" + str(35.99)
	return render_template("table.html", item_name="Chair", item_price=item_price)

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
	app.run('0.0.0.0', port=8000, ssl_context='adhoc')		