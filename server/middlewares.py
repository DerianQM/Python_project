import zlib



def compression_middleware(func):
    def wrapper(request, *args,**kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request,*args,**kwargs)
        return zlib.compress(b_response)
    return wrapper
