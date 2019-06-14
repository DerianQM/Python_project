import yaml
import socket
from argparse import ArgumentParser
import json
import datetime
import hashlib
from datetime import datetime
import zlib
parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file'
)

args = parser.parse_args()

host = 'localhost'
port = 7777
buffersize = 1024
encoding = 'utf-8'



if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

try:
    sock = socket.socket()
    sock.connect((host, port))
    print('Client started')
    action = input('Enter action: ')
    data = input('Enter data: ')
    hash_obl = hashlib.sha3_256()
    hash_obl.update(
        (str(datetime.now().timestamp()).encode(encoding))
    )
    request = {
        'action':action,
        'data': data,
        'time': datetime.now().timestamp(),
        'user': hash_obl.hexdigest()

    }
    s_request = json.dumps(request)
    b_request = zlib.compress(s_request.encode(encoding))
    sock.send(b_request)
    response = sock.recv(buffersize)
    zobj = zlib.decompressobj()
    b_response = zobj.decompress(response)
    print(b_response.decode(encoding))

except KeyboardInterrupt:
    pass