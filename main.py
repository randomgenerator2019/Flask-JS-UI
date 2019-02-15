'''
This is the main working file for this application
'''

#- standard library imports
import argparse
import sys
import ctypes
import platform
import logging
from time import sleep
from threading import Thread, Lock

#- 3rd party library imports
from cefpython3 import cefpython as cef
from views import run_views


views_lock = Lock()
logger = logging.getLogger(__name__)

def url_ping(url, port):
    '''
    Ping the views server on interval
    :param url: str() loca
    :param port:
    :return:
    '''
    try:
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection

    try:
        conn = HTTPConnection(url, port)
        conn.request("GET", "/")
        r = conn.getresponse()
        return r.status == 200
    except:
        logger.exception("Views not started")
        return False

def check_version():
    ver = cef.GetVersion()
    print("CEF Python {ver}".format(ver=ver["version"]))
    print("Chromium {ver}".format(ver=ver["chrome_version"]))
    print("CEF {ver}".format(ver=ver["cef_version"]))
    print("Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"

def initialize_chromium():
    '''
    Initializes Chrome browser window which requires no 3rd party UI libraries
    :return: message loop
    '''
    # source https://github.com/cztomczak/cefpython/blob/master/examples/snippets/window_size.py
    check_version()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    window_info = cef.WindowInfo()
    parent_handle = 0

    # This call has effect only on Mac and Linux.
    # All rect coordinates are applied including X and Y parameters.
    window_info.SetAsChild(parent_handle, [0, 0, 900, 640])
    browser = cef.CreateBrowserSync(url="http://127.0.0.1:23948/login",
                                    window_info=window_info,
                                    window_title="Flask Standalone Web App - Chromium Edition")

    if platform.system() == "Windows":
        window_handle = browser.GetOuterWindowHandle()
        insert_after_handle = 0
        # X and Y parameters are ignored by setting the SWP_NOMOVE flag
        SWP_NOMOVE = 0x0002
        # noinspection PyUnresolvedReferences
        ctypes.windll.user32.SetWindowPos(window_handle, insert_after_handle,
                                          0, 0, 900, 640, SWP_NOMOVE)

    cef.MessageLoop()
    del browser
    cef.Shutdown()


if __name__ == '__main__':
    logger.debug("Starting Views")
    t = Thread(target=run_views)
    t.daemon = True
    t.start()

    logger.debug("Views started")
    if sys.argv[-1] == 'web':
        t.join()
    else:
        logger.debug("Checking Views")
        while not url_ping("127.0.0.1", 5000):
            sleep(0.1)
        initialize_chromium()