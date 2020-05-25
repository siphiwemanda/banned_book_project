import json
from flask import request, _request_ctx_stack, abort, session, redirect
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import constants

AUTH0_DOMAIN = 'banned-book-project.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'logins'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'incorrect authorisations header.'
        }, 400)

    auth_headers = request.headers['Authorization']
    header_parts = auth_headers.split(' ')

    if len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'incorrect authorisations header.'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'incorrect authorisations header.'
        }, 401)
    print(header_parts[1])
    return header_parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def user_in_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            # TODO add a login page
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if constants.JWT in session:
                print('in seesion')
                token = session[constants.JWT]
            else:
                token = get_token_auth_header()

            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
