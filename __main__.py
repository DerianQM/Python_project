import yaml
import socket
from argparse import ArgumentParser
import json
import logging
from actions import resolve
from protocol import validate_request,make_response
from logging.handlers import TimedRotatingFileHandler
import os
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


def get_filename(filename):

    log_directory = os.path.split(filename)[0]


    date = os.path.splitext(filename)[1][1:]

    filename = os.path.join(log_directory, date)

    if not os.path.exists('{}.log'.format(filename)):
        return '{}.log'.format(filename)


    index = 0
    f = '{}.{}.log'.format(filename, index)
    while os.path.exists(f):
        index += 1
        f = '{}.{}.log'.format(filename, index)
    return f


rotation_logging_handler = TimedRotatingFileHandler('./logs/server.log', when='m', interval=1, backupCount=5)
rotation_logging_handler.suffix = '%Y%m%d'
rotation_logging_handler.namer = get_filename


logger = logging.getLogger('main')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(pathname)s -%(module)s - %(message)s')

rotation_logging_handler.setFormatter(formatter)
rotation_logging_handler.setLevel(logging.DEBUG)

logger.addHandler(rotation_logging_handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

try:
    sock = socket.socket()

    sock.bind((host, port))
    sock.listen(5)
    logger.info(f'Server was started with {host} : {port}')


    while True:
        client, address = sock.accept()
        b_request = client.recv(buffersize)
        request = json.loads(b_request.decode(encoding))

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    response = controller(request)
                except Exception as err:
                    logger.critical(err)
                    response = make_response(request,500,'Internal server error')
            else:
                logger.error(f'404 - request:{request}')
                response = make_response(request, 404, 'Action nof found')

        else:
            logger.error(f'400 - request:{request}')
            response = make_response(request,400,'Wrong request')
        s_response = json.dumps(response)
        client.send(s_response.encode(encoding))
        client.close()
except KeyboardInterrupt:
    pass
