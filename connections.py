# -*- coding: utf-8 -*-
"""AIW Base Framework

-*- connections.py -*-

This module includes functions for sending requests and connecting via
socket to the logging microservice. 

Attributes:
    
    This file consists of generic functions that are not to be modified. The
    logToServer function is used to send activity and exception logs to the
    logging microservice.

Creators:
    Names: Ehfaz & Shane
    Date of last edit: 24/10/2019
"""
#Your code starts from here

# Imports

import config
import asyncio
import ssl
import websockets
import pathlib
import json

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)

async def logToServer(message, botName, functionName, success):

    """
    logToServer async function that sends logs to logging microservice.

    Args:
        message: The String that describes the activity to be logged.
        botName: Name of the bot from where the log is being generated.
        functionName: Name of the function from where the log is being generated.
        success: Boolean flag that declares whether or not the activity completed
                 successfully.

    Returns:
        No return value.

    """

    uri = config.LOGGING_SERVER_URL
    clientName = config.CLIENT_NAME

    data = {}
    data['message'] = message
    data['botName'] = botName
    data['functionName'] = functionName
    data['clientName'] = clientName
    data['success'] = success

    dataToSend = json.dumps(data)

    async with websockets.connect(
        uri, ssl_context
    ) as websocket:
        await websocket.send(dataToSend)