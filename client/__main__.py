import yaml
import socket
from argparse import ArgumentParser
import json
import datetime


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
    dct = {
        "action": "presence",
        "time":'',
        "type":"status",
        "user":{
                "account_name":  "C0deMaver1ck",
                "status":"Yep, I am here!"
        },}

    dct["time"] = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')
    data = json.dumps(dct)
    sock.send(data.encode(encoding))
    response = sock.recv(buffersize)
    print(response.decode(encoding))

except KeyboardInterrupt:
    pass