import socket
import subprocess

from ..config import FREEZE_DESTINATION


def serve_build():
    """ Server a build locally """
    process = None
    try:
        process = subprocess.Popen(
            'python -m http.server',
            cwd=FREEZE_DESTINATION,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print('http://{0}:8000'.format(socket.gethostbyname(socket.gethostname())))
        input('Press enter to stop the server')
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if process is not None:
            process.terminate()
