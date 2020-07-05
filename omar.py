import tensorflow as tf
import tensorflow_hub as hub
from flask import Flask, request,make_response
from flask_restful  import Resource, Api
import os
import sys
import json
from json import JSONEncoder
import numpy

app = Flask(__name__)
api = Api(app)
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class GenerateEmbed(Resource):
    def __init__(self):
        self.embed_fn = self.embed_useT(os.getcwd()+'/module_useT')  # loading the model #------> rasmy
    def post(self):
        Body = request.get_json()
        if "Text" in Body:
            try:
                numpyData = {"Text": self.embed_fn(Body.get("Text"))}
                encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
                return make_response(encodedNumpyData)
            except:
                print(sys.exc_info())
                return make_response("Some Attribute missed ", 404)

    def embed_useT(self,module):
        with tf.Graph().as_default():
            sentences = tf.placeholder(tf.string)
            embed = hub.Module(module)
            embeddings = embed(sentences)
            session = tf.train.MonitoredSession()
        return lambda x: session.run(embeddings, {sentences: x})



api.add_resource(GenerateEmbed, '/GenerateEmbed')  # Route_1
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)