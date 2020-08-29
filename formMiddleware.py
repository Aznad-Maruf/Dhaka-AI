from werkzeug.wrappers import Request, Response, ResponseStream

class FormMiddleware():
    def __init__(self, app):
        self.app = app
        self.name = "init"
    
    def __call__(self, environ, start_response):
        request = Request(environ)

        name = request.form.get('name')
        # email = request.form['email']
        # temp = {'name':name, 'email':email}

        environ['test'] = {
            'name': name
        }
        
        return self.app(environ, start_response)

        # res = Response('SEcond one', mimetype='text/plain', status=401)
        # return res(environ, start_response)