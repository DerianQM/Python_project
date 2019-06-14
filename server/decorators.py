import logging
from functools import wraps
from protocol import make_response
import datetime

logger = logging.getLogger('decorators')



def logger_required(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        logger.debug(f'{func.__name__} : {request}')
        return func(request,*args,**kwargs)
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'user' in request:
            return func(request, *args, **kwargs)
        return make_response(request,403,'Access denied')
    return wrapper

def logs(func):
    def wrapper(request, *argv, **kwargv):
        saved_args = locals()
        logging.info(f'Время вызова - "{datetime.datetime.now().strftime("%Y-%m-%d_%H%M") }" Модуль вызова - "{func.__module__}" - Bмя вызванной функции - "{func.__name__} " ее параметры - {saved_args}')
        return func(request, *argv, **kwargv)
    return wrapper