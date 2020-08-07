import subprocess

from ..config import FREEZE_DESTINATION


def serve_build(port: int):
    """ Server a build locally """
    process = None
    try:
        process = subprocess.Popen(
            f'python -m http.server {port}',
            cwd=FREEZE_DESTINATION,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f'http://localhost:{port}')
        input('Press enter to stop the server')
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if process is not None:
            process.terminate()
