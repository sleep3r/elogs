from config import settings_setup
from channels.routing import get_default_application
import os
import time
import traceback
import signal
import sys

try:
    application = get_default_application()
except Exception:
    print('handling WSGI exception')
    traceback.print_exc()
    os.kill(os.getpid(), signal.SIGINT)
    time.sleep(2.5)
