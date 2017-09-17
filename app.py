from flask import Flask, render_template, request
import unirest, json, uuid
from models import Session, Account, Item
from OpenSSL import SSL

app = Flask(__name__)
session = Session()

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
    items = session.query(Item).order_by(Item.id.asc()).all()
    return render_template("dashboard.html", items=items)

# Display buyer page to connect accounts for Coinbase and Square, see history/info/etc
@app.route('/buyer')
def buyer():
	return render_template("paymentForm.html", application_id = square_application_id, postal_code="94103",expiration_date="04/20",card_number="4532759734545858",cvv="111")

# Display item info
@app.route('/item/<int:item_id>')
def display_item_info(item_id):
	item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
                return 'No item found.'
	return render_template("table.html", item_name=item.name, item_price=item.price)

@app.route('/reset')
def reset():
        session.query(Item).update({"sold": 0})
        session.commit()
        return 'reset'

@app.route('/add/<int:item_id>', methods=['GET', 'POST'])
def add(item_id):
        session.query(Item).filter(Item.id == item_id).update({"sold": Item.sold + 1})
        session.commit()

        return 'All good in the hood! :)'

@app.route('/remove/<int:item_id>', methods=['POST'])
def remove(item_id):
        session.query(Item).filter(Item.id == item_id).update({"sold": Item.sold - 1})
        session.commit()
        return 'OK'

@app.route('/cart')
def cart():
        items = [{"total": i.sold * i.price, "count": i.sold,
                  "name": i.name, "price": i.price} for i in session.query(Item).all()]
        return render_template("cart.html", items=items)

# Execute payment through Square API
@app.route('/pay/square', methods=['GET','POST'])
def square():
	
	# Sandbox Location ID (Coffee & Toffee NYC)
	card_nonce = 'CBASEO_uJKUcQWA6Kjz-RiJZs7cgAQ'
	if request.form:
		card_nonce = request.form
		print("card nonce: ", card_nonce)
	location_id = 'CBASEEKdEq0dwQd9aigzQlUVGhYgAQ'
	#card_nonce = 

	items = [{"total": i.sold * i.price} for i in session.query(Item).all()]

	response = unirest.post('https://connect.squareup.com/v2/locations/' + location_id + '/transactions',
		headers={
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + square_access_token,
		},
		params = json.dumps({
			'card_nonce': card_nonce,
			'amount_money': {
			        'amount': int(100 + items[0]['total']),
			        'currency': 'USD'
			},
			'idempotency_key': str(uuid.uuid1())
		})
	)

	return json.dumps(response.body)


# Execute payment through Coinbase API
@app.route('/pay/coinbase/<int:item_id>', methods=['GET','POST'])
def coinbase(item_id):
	pass

if __name__ == "__main__":
	app.debug = True
	app.run('0.0.0.0', port=8000, ssl_context='adhoc')		
