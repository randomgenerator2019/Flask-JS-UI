'''
This is intended for all python endpoint backend tasks
'''

import os

# Use this for calls to outside libraries and system based functions


def system_os_call():
    '''
    Simple function to return a basic os call.
    :return: str() the current working directory
    '''

    return str(os.getcwd())

