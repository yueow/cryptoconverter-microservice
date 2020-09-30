import hmac
from functools import wraps

from django.conf import settings


class SignVerifyError(Exception):
    pass
# Request does not have 'Sign' in headers
class SignRequestEmpty(SignVerifyError):
    pass
# 'Sign' does not match
class SignDoesNotMatch(SignVerifyError):
    pass


# Generate HMAC 'Sign'
def generate_sign(msg):
    msg = msg.encode('utf-8')
    return hmac.new(bytes(settings.API_KEY, encoding='utf-8'), msg, digestmod=settings.SIGN_DIGESTMOD).hexdigest()

# Formating a message(e.g. ’2BTCUSDT’)    
# 'obj' could be a dict or request.POST
def comb_sign_string(obj):
    data = {key: value for key, value in obj.items()}
    msg = ''.join(sorted(data.values()))
    return msg

# Verify 'Sign' in Request
def verify_sign_request(request):
    # Checks an existing 'sign' header in request
    # If 'sign' does not exist, it raises exception
    request_sign = request.headers.get('Sign', None)
    if not request_sign:
        raise SignRequestEmpty('The request unsigned')

    msg = comb_sign_string(request.POST)
    # print(generate_sign(msg))
    
    # Verifying request
    # If request 'Sign' does not match to generated sign, it raises exception
    if hmac.compare_digest(request_sign, generate_sign(msg)):
        return request
    else:
        raise SignDoesNotMatch('Request sign is not verified!')

# Assign 'Sign' to Response
def sign_reponse(response, msg):
    # If we use JsonResponse it raise AttributeError Exception 
    #   and it passes 'Sign' into response object
    try:
        response.headers['Sign'] = generate_sign(msg)
    except AttributeError:
        response['Sign'] = generate_sign(msg)
    return response