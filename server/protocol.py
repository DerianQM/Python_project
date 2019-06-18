import datetime

def validate_request(raw):
    if 'time' and 'action' in raw:
        return True

    return False

def make_response(request,code,date= None):
    return {
        'action': request.get('action'),
        'user': request.get('user'),
        'time': datetime.datetime.now().strftime('%Y-%m-%d_%H%M'),
        'data': date,
        'code': code
    }