#!/usr/bin/env python3
import zmq

from search.manager import image_search_manager
import conf

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(conf.SEARCH_WORKER_ZMQ_ENDPOINT)

while True:
    msg = socket.recv_json()

    result = {
        'data': [img.as_dict() for img in image_search_manager.search(msg['filename'])]
    }

    socket.send_json(result)

