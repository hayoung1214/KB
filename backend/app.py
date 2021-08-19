# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
# from bson import json, json_util
from flask_restx import Resource, Api, fields, reqparse
from flask_cors import CORS
from kakaokey import KAKAO_KEY 
import os
from werkzeug.datastructures import FileStorage
from detection import predict

app = Flask(__name__)
api = Api(app, version='1.0', title='KB API',
          description='KB REST API 문서')
ns = api.namespace('api/v1/user', description='user 관련 API 목록')
ns2 = api.namespace('api/v1/message', description='message 관련 API 목록')

CORS(app, supports_credentials=True)


logout_parser = ns.parser()
mdetect_parser = ns2.parser()
mshow_parser = ns2.parser()


@ns2.route('/detect')
class detect(Resource):

    mdetect_parser.add_argument(
        'message', type=str, required=True, location='json', help="메세지")
    
    @ns2.expect(mdetect_parser)
    @ns2.response(201, '확인해보고 싶은 메세지 등록 성공')
    @ns2.response(400, 'Bad Request')
    @ns2.response(401, 'INVALID_USER')

    def post(self):
        
        try :
            args = mdetect_parser.parse_args()
            # clinet_id = request.headers['client_id'] 회원가입 기능 추가한다면 넣기
            
            message = args['message']
            
            print("message : ", message)
            
            # 모델 넘기는 부분 추가하기
            result = predict(message)
            print("result : ", result)
            
            data = {
                "success": True,
                "message": "확인해보고 싶은 메세지 등록 성공",
                "result" : result
            }

            response = jsonify(data)
            response.status_code = 201
            return response
       
        except KeyError:
            data = {
                    "message": "INVALID_USER"
            }
            response = jsonify(data)
            response.status_code = 401
            return response



# app.run(host='0.0.0.0',debug=True)
if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', debug=True)