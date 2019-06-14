import json
import logging
from decorators import logs
from actions import resolve
from protocol import( validate_request, make_response )
from middlewares import compression_middleware


@compression_middleware
@logs
def handle_default_request(raw_request):
    request = json.loads(
        raw_request.decode()
    )

    if validate_request(request):
        action_name = request.get('action')
        controller = resolve(action_name)
        if controller:
            try:
                response = controller(request)
            except Exception as err:
                logging.critical(err)
                response = make_response(request, 500, 'Internal server error')
        else:
            logging.error(f'404 - request:{request}')
            response = make_response(request, 404, 'Action nof found')

    else:
        logging.error(f'400 - request:{request}')
        response = make_response(request, 400, 'Wrong request')

    return json.dumps(response).encode()