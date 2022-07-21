import base64
import json
import os
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer, ThreadingMixIn
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class HTTPServer(ThreadingMixIn, TCPServer):
    daemon_threads = True
    key = None

    def set_auth(self, username, password):
        self.key = base64.b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


def load_file(file):
    with open(file, 'rb') as file_handler:
        return file_handler.read()


def serve_on_port(port, command, user, pwd):
    HTTPHandler.os_command = command
    server = HTTPServer(('0.0.0.0', port), HTTPHandler)
    if user is not None and pwd is not None:
        server.set_auth(user, pwd)
    print("Serving at localhost:{}".format(port))
    server.serve_forever()


class HTTPHandler(BaseHTTPRequestHandler):
    os_command = None

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="CC Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') is None and key is not None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        elif self.headers.get('Authorization') == 'Basic ' + str(key) or key is None:
            if self.path == '/img':
                os.system(self.os_command)
                data = load_file(imageName)
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Content-Disposition', "inline; filename={}".format(imageName))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Url not found...')


# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--user", default=None, help="Username")
parser.add_argument("-pwd", "--password", default=None, help="Password")
parser.add_argument("-p", "--port", default=8080, type=int, help="Port")
parser.add_argument("-f", "--frames", default=4, type=int, help="Number of frames to capture")
parser.add_argument("stream_url", help="Stream URL")
args = vars(parser.parse_args())

PORT = args["port"]
USER = args["user"]
PWD = args["password"]
imageName = "snap.jpg"
streamLink = args["stream_url"]
frames = args["frames"]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ffmpeg_command = "ffmpeg -rtsp_transport tcp -err_detect aggressive -fflags discardcorrupt -v fatal -y -i {} " \
                     "-frames:v {} -r 1 -an -f image2 -update 1 {}".format(streamLink, frames, imageName)
    serve_on_port(PORT, ffmpeg_command, USER, PWD)
