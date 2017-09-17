from flask import Flask, render_template
import unirest, json, uuid
from models import Account, Item

app = Flask(__name__)

################
### API Keys ###
################

square_application_id = 'sandbox-sq0idp-NMjTA4x9HyDSGNWXdwc2Pg'
square_access_token = 'sandbox-sq0atb-VGm6YqbVmufgp9MHE3j1FQ'

##############
### Routes ###
##############

# Display seller dashboard with statistics
@app.route('/')
@app.route('/seller')
def seller():
	# revenue = calculateRevenue()
	def callback(session):
		return render_template("dashboard.html", items=session.query(Item).order_by(Item.id.asc()).all())

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