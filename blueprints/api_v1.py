'''
Intended to be the Swagger REST API hooking into models, backend.launch & backend.query
which should return a {'result':"*result of backend task*"} to the API
'''

#- standard library imports

#- 3rd party library imports
from flask import Flask, render_template, jsonify, request, url_for, Blueprint
from flask_restplus import Resource, Api, fields
import backend.launch as launch
from models import demo

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


#-----------
# Model Object API
#-----------

# Assign a namespace for better vieing in swagger UI
model_object_namespace = api.namespace('Model Object', description='Demo of the model object interaction')

# Define the model and assign api
model = demo.ModelObject(api)

# Marshal the model
model_marshal = api.model('model_object_marshal', {
    'id': fields.Integer(readOnly=True, description='The model_object_marshal unique identifier'),
    'content': fields.String(required=True, description='Basic demo content of model_object '),
})

# Create a dummy model
model.create({'id':1,'content':'this is the first item in model_object'})

# Define a route for swagger UI to interact with the demo.ModelObject
@api.route('model_object')
@api.response(404, 'model not found')
@api.param('id', 'The model identifier')
@api.param('content', 'String contents of model_object')
class ApiModelObject(Resource):
    '''Show a single model item and lets you delete them'''

    @api.doc('get_model')
    @api.marshal_with(model_marshal)
    def get(self, id):
        '''Fetch a given resource'''
        return model.get(id)

    @api.doc('delete_model')
    @api.response(204, 'model deleted')
    def delete(self, id):
        '''Delete a model given its identifier'''
        model.delete(id)
        return '', 204

    @api.expect(model_marshal)
    @api.marshal_with(model_marshal)
    def put(self, id):
        '''Update a model given its identifier'''
        return model.update(id, api.payload)

# Append this Namespace to main API blueprint
api.add_namespace(model_object_namespace)




