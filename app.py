from flask import Flask, request
from flask_restful import Api, Resource
from auth import Authentication
from kaspersky.kaspersky import Kaspersky
from etpos.etpos import Etpos
from hr.hr import Hr

app = Flask(__name__)
api = Api(app)


# Login Request
class login(Resource):
    def post(self):
        auth = request.authorization
        return Authentication.login(auth)


# Kaspersky Requests
class Createsub(Resource):
    def post(self):
        data = request.get_json()
        auth = request.authorization
        return Kaspersky.create_sub(data, auth)


class Modifysub(Resource):
    def post(self):
        data = request.get_json()
        auth = request.authorization
        return Kaspersky.modify_sub(data, auth)


class Removesub(Resource):
    def post(self):
        data = request.get_json()
        auth = request.authorization
        return Kaspersky.remove_sub(data, auth)


# Etpos Requests
class Registermerchant(Resource):
    def post(self):
        data = request.get_json()
        auth = request.authorization
        return Etpos.register_merchant(data, auth)


class Createstore(Resource):
    def post(self):
        data = request.get_json()
        auth = request.authorization
        return Etpos.create_store(data, auth)


# Hr Requests
class Requesttoken(Resource):
    def post(self):
        data = request.get_json()
        return Hr.requet_token(data)


class Getleave(Resource):
    def get(self):
        data = request.get_json()
        return Hr.requet_leave(data)


# Login Request
api.add_resource(login, '/api/login/')

# Kaspersky Routes
api.add_resource(Createsub, '/api/kasperskey/createsub/')
api.add_resource(Modifysub, '/api/kasperskey/modifysub/')
api.add_resource(Removesub, '/api/kasperskey/removesub/')

# Etpos Routes
api.add_resource(Registermerchant, '/api/etpos/registermerchant/')
api.add_resource(Createstore, '/api/etpos/createstore/')

# HR Routes
api.add_resource(Requesttoken, '/api/hr/requesttoken/')
api.add_resource(Getleave, '/api/hr/getleave/')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
