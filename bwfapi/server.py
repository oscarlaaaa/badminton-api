from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"about": "Hello World!"}
    
    def post(self):
        return {"you sent" : request.get_json()}

api.add_resource(HelloWorld, '/')

if __name__ == "__main__":
    app.run(debug=True)