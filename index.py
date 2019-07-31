from flask import Flask, abort, request
import json

import test_call
import get_campaigns

import add_display_ad
import add_search_ad
import change_campaign_state
import create_account
import create_ad_group
import get_report
import get_adgroups
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_campaigns/', methods=['POST']) # works
def handler_get_campaigns():
	return get_campaigns.main(request.json)

@app.route('/get_ad_groups/', methods=['POST']) # works
def handler_get_adgroups():
	return get_adgroups.main(request.json)

@app.route('/create_ad_groups/', methods=['POST']) # works
def handler_create_ad_groups():
	return create_ad_group.main(request.json)

@app.route('/create_campaign/', methods=['POST']) # needs testing
def handler_create_campaign():
	return test_call.main(request.json)

@app.route('/create_account/', methods=['POST']) # needs testing
def handler_create_account():
	return create_account.main(request.json)

@app.route('/change_campaign_state/', methods=['POST', 'GET']) # works
@cross_origin()
def handler_change_campaign_state():
	return change_campaign_state.main(request.json)

@app.route('/create_text_ad/', methods=['POST']) # needs testing
def handler_create_text_ad():
	return add_search_ad.main(request.json)

@app.route('/create_display_ad/', methods=['POST']) # needs testing
def handler_create_display_ad():
	return add_display_ad.main(request.json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
