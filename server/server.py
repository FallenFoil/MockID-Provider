import time
import json
import random
import jwt

from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime, timezone
from urllib.parse import unquote

tenants = ['fallencoil']

authCodes = {
  'CpLcpMOOpjiBZOEpHTIuSSuWDdVeyzCr': {'sub': 'User 1',  'name': 'Luis Macedo',      'iat': int(time.time()), 'email': 'luis@macedo.com'},
  'rkZMvQVDrlrpTGIxAygwUrcIaoEZiIFL': {'sub': 'User 2',  'name': 'Pedro Fernandes',  'iat': int(time.time()), 'email': 'pedro@fernandes.com'},
  'HMfBnHRzAowBLFYWsBZfZaSeTYuAGlPf': {'sub': 'User 3',  'name': 'Ricardo Azevedo',  'iat': int(time.time()), 'email': 'ricardo@azevedo.com'},
  'fDuyOGFjZBsRaWZmiRkJlnOkblgoJBkm': {'sub': 'User 4',  'name': 'Francisco Melo',   'iat': int(time.time()), 'email': 'francisco@melo.com'},
  'bjiTSeIJfVpCYIChjbXohngVFpKUHNcd': {'sub': 'User 5',  'name': 'Duarte Cruz',      'iat': int(time.time()), 'email': 'duarte@cruz.com'},
  'eGtEosiubDKxFmNETLcCWtTnGHMenwSQ': {'sub': 'User 6',  'name': 'Gonçalo Afonso',   'iat': int(time.time()), 'email': 'gonçalo@afonso.com'},
  'AYqgJrtOcDVBkAvGTBintFcXeUMfEDaG': {'sub': 'User 7',  'name': 'Nuno Rodrigues',   'iat': int(time.time()), 'email': 'nuno@rodrigues.com'},
  'HjiyBwpapiaZQriFRwPfoGPJzKFXJvaq': {'sub': 'User 8',  'name': 'Ricardo Candeias', 'iat': int(time.time()), 'email': 'ricardo@candeias.com'},
  'CHAexyJeXypVAaCvFbFMdXgPHfunWFDZ': {'sub': 'User 9',  'name': 'Pedro Henriques',  'iat': int(time.time()), 'email': 'pedro@henriques.com'},
  'OPXZkGfqHftzFPxiaSxuiZuJcwzJSVEA': {'sub': 'User 10', 'name': 'Joao Sousa',       'iat': int(time.time()), 'email': 'joao@sousa.com'}
}

class JWTHandler:
  def __init__(self):
    with open('/openid/keys/id_rsa', 'r') as file:
      self.privateKey = file.read()
    with open('/openid/keys/id_rsa.pub', 'r') as file:
      self.publicKey = file.read()

  def encodeJWT(self, data):
    encoded = jwt.encode(data, self.private_key, algorithm="RS256")
    return encoded

  def decodeJWT(self, token):
    decoded = jwt.decode(token, self.public_key, algorithms=["RS256"])
    return decoded

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
  def __init__(self, *args):
    self.jwtHandler = JWTHandler()
    super().__init__(*args)

  def parseQueryParams(self, paramsRaw):
    paramsProcessed = {}
    params = paramsRaw.split('&')

    for param in params:
      paramParts = param.split('=', 1)
      paramsProcessed[paramParts[0]] = paramParts[1]

    return paramsProcessed

  def do_GET(self):
    paths = self.path.split('/')[1:]

    if len(paths) < 2:
      payloadRaw = {'error': 'URL malformed', 'error_description': 'URL malformed. Try /<tenant>/<endpoint>'}
    else:
      tenant = paths[0]
      authEndpoint = paths[1]

      if tenant in tenants:
        authEndpointParts = authEndpoint.split('?', 1)
        authEndpoint = authEndpointParts[0]
        if authEndpoint == 'authorize':
          queryParams = []
          if len(authEndpointParts) == 2:
            queryParams = self.parseQueryParams(authEndpointParts[1])
          print('Authorize')
          time.sleep(10)
          self.send_response(301)
          self.send_header('Location', unquote(queryParams['redirect_uri']) + '?code=' + list(authCodes.keys())[random.randint(0, 9)])
          self.end_headers()
          return
        else:
          payloadRaw = {'error': 'Endpoint not recognized', 'error_description': 'Endpoint not recognized'}
      else:
        payloadRaw = {'error': 'Tenant does not exist', 'error_description': 'Tenant does not exist'}

    payload = json.dumps(payloadRaw)

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_header('Content-Length', len(payload))
    self.send_header('Date', datetime.now(timezone.utc))
    self.end_headers()

    self.wfile.write(bytes(payload, 'utf-8'))

  def do_POST(self):
    paths = self.path.split('/')[1:]

    if len(paths) < 2:
      payloadRaw = {'error': 'URL malformed', 'error_description': 'URL malformed'}
    else:
      tenant = paths[0]
      authEndpoint = paths[1]

      if tenant in tenants:
        authEndpointParts = authEndpoint.split('?', 1)
        authEndpoint = authEndpointParts[0]
        if authEndpoint == 'token':
          requestBodyLength = int(self.headers.get('Content-Length'))
          requestBody = self.rfile.read(requestBodyLength)
          print(requestBody)
          # data = authCodes[requestBody['code']]
          # jwtToken = self.jwtHandler.encodeJWT(data)
          jwtToken = ''

          payloadRaw = {'access_token': jwtToken}
        else:
          payloadRaw = {'error': 'Endpoint not recognized', 'error_description': 'Endpoint not recognized'}
      else:
        payloadRaw = {'error': 'Tenant does not exist', 'error_description': 'Tenant does not exist'}

    payload = json.dumps(payloadRaw)

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_header('Content-Length', len(payload))
    self.send_header('Date', datetime.now(timezone.utc))
    self.end_headers()

    self.wfile.write(bytes(payload, 'utf-8'))
    return

def main():
  PORT = 9000
  Handler = CustomHTTPRequestHandler

  with HTTPServer(('', PORT), Handler) as httpd:
    print('serving at port', PORT)
    httpd.serve_forever()

if __name__ == '__main__':
  main()