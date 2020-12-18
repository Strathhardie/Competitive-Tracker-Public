from flask import Flask, request, jsonify, make_response, send_from_directory
import os
import jwt
from  werkzeug.security import generate_password_hash, check_password_hash 
from os.path import exists, join
from datetime import datetime, timedelta 
from functools import wraps 
from flask_cors import CORS

from constants import CONSTANTS
from sample_data import sample_data

app = Flask(__name__, static_folder='build')
CORS(app)

# Secret Token Key
app.config['SECRET_KEY'] = 'secret_key_test'

# MasterDetail Page Endpoint
@app.route(CONSTANTS['ENDPOINT']['MASTER_DETAIL'])
def get_master_detail():
    return jsonify(sample_data['text_assets'])

# Token Decorator
# decorator for verifying the JWT 
def token_required(f): 
    @wraps(f) 
    def decorated(*args, **kwargs): 
        token = None
        # jwt is passed in the request header 
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token'] 
        # return 401 if token is not passed 
        if not token: 
            return jsonify({'message' : 'Token is missing !!'}), 401
   
        try: 
            # decoding the payload to fetch the stored details 
            data = jwt.decode(token, app.config['SECRET_KEY']) 
            current_user = data['public_id']
        except: 
            return jsonify({ 
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes 
        return  f(current_user, *args, **kwargs) 
   
    return decorated 

# Catching all routes
# This route is used to serve all the routes in the frontend application after deployment.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    file_to_serve = path if path and exists(join(app.static_folder, path)) else 'index.html'
    return send_from_directory(app.static_folder, file_to_serve)

@app.route('/login', methods =['POST']) 
def login(): 
    # creates dictionary of form data 
    auth = request.form 
   
    if not auth or not auth.get('username') or not auth.get('password'): 
        # returns 401 if any email or / and password is missing 
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
        ) 
    
    if auth.get('username') != CONSTANTS['USERNAME']: 
        # returns 401 if user does not exist 
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'} 
        ) 
   
    if check_password_hash(CONSTANTS['PASSWORD'], auth.get('password')): 
        # generates the JWT Token 
        token = jwt.encode({ 
            'public_id': CONSTANTS['USERNAME'], 
            'exp' : datetime.utcnow() + timedelta(minutes = 30) 
        }, app.config['SECRET_KEY']) 
   
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201) 
    # returns 403 if password is wrong 
    return make_response( 
        'Could not verify', 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
    ) 

@app.route('/test', methods =['GET'])
@token_required
def test(current_user):
    return jsonify({'success' : True})

# Error Handler
@app.errorhandler(404)
def page_not_found(error):
    json_response = jsonify({'error': 'Page not found'})
    return make_response(json_response, CONSTANTS['HTTP_STATUS']['404_NOT_FOUND'])

if __name__ == '__main__':
    app.run(port=CONSTANTS['PORT'])
