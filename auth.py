from functools import wraps

from flask import current_app, request, make_response

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            username = current_app.config['AUTH_USERNAME']
            password = current_app.config['AUTH_PASSWORD']
            if auth.username == username and auth.password == password:
                return f(*args, **kwargs)
            
        return make_response('Authorization failed', 401, {
            'Www-Authenticate': 'Basic realm="Login Required"'
        })
    
    return decorated
