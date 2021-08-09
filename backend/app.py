from flask import Flask, jsonify, request, session, Response
from werkzeug.utils import secure_filename
from bson.json_util import json
from flask_restx import Resource, Api, fields, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app, version='1.0', title='KB API',
          description='KB REST API 문서')
ns = api.namespace('api/v1/user', description='user 관련 API 목록')
ns2 = api.namespace('api/v1/message', description='message 관련 API 목록')

CORS(app, supports_credentials=True)

login_parser = ns.parser()
mupload_parser = ns2.parser()
mshow_parser = ns2.parser()

