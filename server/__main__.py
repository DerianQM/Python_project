import json
import yaml
import socket
import select
import logging
from argparse import ArgumentParser

from actions import resolve
from handlers import handle_default_request
from protocol import (
    make_response,  validate_request
)


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

# logger = logging.getLogger('main')
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler = logging.FileHandler('main.log')

# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.DEBUG)

# logger.addHandler(file_handler)
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding=encoding),
        logging.StreamHandler()
    ]
)

requests = []
connections = []

try:
    sock = socket.socket()

    sock.bind((host, port))
    sock.setblocking(True)
    sock.listen(5)
    print(f'Server was started with {host}:{port}')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Client with address {address} was detected.')
            connections.append(client)
        except:
            pass

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for r_client in rlist:
            b_request = r_client.recv(buffersize)
            requests.append(b_request)

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_client.send(b_response)
except KeyboardInterrupt:
    pass