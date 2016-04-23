import flask
from flask.ext import restful
from bson.json_util import dumps
from flask.ext.cors import CORS
from flask_mongoengine import MongoEngine
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
app.config.from_object(__name__)
app.config['TESTING'] = True
app.config['MONGODB_SETTINGS'] = {'host': '0.0.0.0',
                                 'port': 27017,
                                 'db' : 'Trackr_DB'}

app.config["SECRET_KEY"] = 'HonestEngine'
CORS(app, resources = ["*localhost*"])
db = MongoEngine()
db.init_app(app)

def output_json(obj, code, headers=None):
    response = make_response(dumps(obj), code)
    response.headers.extend(headers or {})
    return response

DEFAULT_REPRESENTATIONS = {'application/json': output_json}

@app.route("/")
def index():
    return flask.render_template('index.html')

class air_check(db.Document):
    location = db.StringField(max_length = 100, required = True)
    timestamp = db.StringField(max_length = 40)
    response = db.StringField(max_length = 40)

class user(db.Document):
    user_id = db.StringField(max_length = 40, unique=True, required = True)
    password = db.StringField(max_length = 40, required = True)
    user_email = db.StringField(max_length = 40, unique=True, required = True)
    provider = db.StringField(max_length = 40, unique = True, required = True)
    air_checks = db.ListField(db.ReferenceField(air_check))

    def __unicode__(self):
        return self.user_id

class getUser(restful.Resource):
    
    def get(self, user_id = None):
        data = request.get_json()
        user_id = data.get("user_id")
        user = User.objects.filter(**{"user_id" : user_id}).first()
        if user:
            return jsonify({"status": "ok", "user":user})
        else:
            return jsonify({"status":"fail"})

class loginUser(restful.Resource):

    def get(self, user_id=None, password=None):
        data = request.get_json()
        password = data.get('password')
        user_id = data.get('user_id')
        user = User.objects.filter(**{"user_id" : user_id, "password" : password}).first()
        if user:
            return jsonify({"status": "ok", "log_in": user.user_id})
        else:
            return {"status": "fail"}

class checkNewUser(restful.Resource):

    def get(self, user_id = None, user_email = None):
        data = request.get_json()
        user_id = data.get("user_id")
        user_email = data.get("email")
        taken_user = User.objects.filter(**{"user_id" : user_id}).first()
        taken_email = User.objects.filter(**{"user_email": user_email}).first()
        if (taken_user or taken_email):
            return jsonify({"status":"fail"})
        else:
            return {"status":"ok"}

class postUser(restful.Resource):
    def post(self):
        data = request.get_json()
        if not data:
            data = {"status": "ERROR"}
            return jsonify(data)
        else:
            user_id = data.get('user_id')
            email = data.get('email')
            password = data.get('password')
            provider = data.get('provider')
            if user_id:
                User(user_id=user_id, password = password,user_email=email, provider = provider).save()
            else:
                return jsonify({"response": "registration number missing"})

class add_air_check(restful.Resource):

    def post(self):
        data = request.get_json()
        if not data:
            data = {'status': 'ERROR'}
            return jsonify(data)
        else:
            user_id = data.get('user_id')
            date = data.get('date')
            if user_id:
                user = User.objects.filter(**{'user_id': user_id }).first()
                new_air_check = air_check(
                    gif_file_path = gif_file_path,
                    date = date
                     )
                new_lift.save()
                user.lifts.insert(0, new_lift)
                user.save()
                return jsonify({"status": "ok"})

class get_air_check(restful.Resource):
    def get(self):
        data = request.get_json()
        if not data:
            data = {'status': 'ERROR'}
            return jsonify(data)
        else:
            user_id = data.get('user_id')
            if user_id:
                user = User.objects.filter(**{'user_id': user_id}).first()
                if user:
                    return jsonify({"status" : "ok", "lifts": user.lifts})
                else:
                    return jsonify({"status": "ERROR"})

class deleteUser(restful.Resource):

    def delete(self, user_id = None):
        if user_id is None:
            return jsonify({"response" : "ERROR"})
        else:
            user = User.objects.filter(**{"user_id" : user_id}).first()
            if user is None:
                return jsonify({"response" : "no user with this id"})
            else:
                User.objects.delete(user)

api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS
api.add_resource(getUser, '/User')
api.add_resource(loginUser, '/LoginUser')
api.add_resource(checkNewUser, '/checkNew')
api.add_resource(postUser, '/postUser')
api.add_resource(deleteUser, '/deleteUser')
api.add_resource(add_air_check, '/addAirCheck')
api.add_resource(get_air_check, '/getAirCheck')


if __name__ == "__main__":
    app.debug = True
    app.run()