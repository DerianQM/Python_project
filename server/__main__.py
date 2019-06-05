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

host = '0.0.0.0'
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

    sock.bind((host, port))
    sock.listen(5)
    print(f'Server was started with {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client was detected {address}')
        data = client.recv(buffersize)
        print(data.decode(encoding))
        dct = json.loads(data)
        if dct['action']=='presence':
            data = {"action": "probe",
                     "time":  datetime.datetime.now().strftime('%Y-%m-%d_%H%M'),
                     }

        print(data)
        client.send(json.dumps(data).encode())
        client.close()
except KeyboardInterrupt:
    pass
