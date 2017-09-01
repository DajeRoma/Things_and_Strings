from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import time
import uuid

from TSM import TSM

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


def crossdomain(origin=None, methods=None, headers=None,
				max_age=21600, attach_to_all=True,
				automatic_options=True):

	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, basestring):
		headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, basestring):
		origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()

	def get_methods():
		if methods is not None:
			return methods

		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']

	def decorator(f):
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp

			h = resp.headers

			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp

		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator


# @app.before_request
# def limit_remote_addr():
# 	allowed_ip = ["128.111.106.188"]
# 	"""
# 		Only allow ip in allowed_ip to directly access the API 
# 		  or through the web interface 
# 	"""
# 	if "HTTP_ORIGIN" not in request.environ and request.remote_addr not in allowed_ip:
# 		abort(403)
	# print request.remote_addr
	# print request.environ


# tsm = TSM("", "")
# @app.before_request
# def preload():
# 	tsm = TSM("", "")


@app.route('/')
# @cross_origin(origins='128.111.106.188')
def index():
	return '/search/<sentence>/<placeName>'


@app.route('/ner/<sentence>')
def named_entity_recognition(sentence):
	annotated_word_list, word_list, locations_indices = TSM.named_emtity_recognition(sentence)
	locations = []
	for item in annotated_word_list:
		if item[1] == "LOCATION":
			locations.append(item[0])
	return jsonify({"result": locations})


@app.route('/search/<sentence>/<placeName>')
# @cross_origin(origins='http://www.geog.ucsb.edu')
def searchChem(sentence, placeName):
	tsm = TSM(placeName, sentence)
	result_dict = tsm.call_integration_model()
	return jsonify({"result": result_dict})



if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port = 2222, use_reloader=True, threaded=False)