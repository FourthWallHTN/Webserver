from flask import Flask, render_template
import unirest, json, uuid
app = Flask(__name__)

square_application_id = 'sandbox-sq0idp-NMjTA4x9HyDSGNWXdwc2Pg'
square_access_token = 'sandbox-sq0atb-VGm6YqbVmufgp9MHE3j1FQ'

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
@app.route('/pay/square/<item>')
def square(item):

	# Sandbox Location ID (Coffee & Toffee NYC)
	location_id = 'CBASEEKdEq0dwQd9aigzQlUVGhYgAQ'
	card_nonce = 'FAKE_CARD_NONCE'

	response = unirest.post('https://connect.squareup.com/v2/locations/' + location_id + '/transactions',
		headers={
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + access_token,
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

	return 0

# Execute payment through Coinbase API
@app.route('/pay/coinbase/<item>')
def coinbase():
	pass

if __name__ == "__main__":
	app.debug = True
	app.run('0.0.0.0', port=8000)