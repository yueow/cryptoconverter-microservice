import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from currencyconverter import sign
from currencyconverter.converter import CurrencyConverter


# @verify_sign
@csrf_exempt
@require_http_methods(["POST"])
def convert_currency_view(request):
    # Verifying Request object
    try:
        request = sign.verify_sign_request(request)
    except sign.SignVerifyError as err:
        return JsonResponse({'message':f'Oops: {err}'})
    
    # Converter takes request.POST or any dict
    converter = CurrencyConverter(request.POST)

    # Subscribing Response object
    signed_response = sign.sign_reponse(
        JsonResponse({
            'out_amount': converter.int_convert(),
            'rate': converter.get_int_rate(),
        }), 
        sign.comb_sign_string(request.POST)
        )
    return signed_response