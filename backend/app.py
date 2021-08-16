# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, session, Response, render_template, redirect
from werkzeug.utils import secure_filename
# from bson import json, json_util
from flask_restx import Resource, Api, fields, reqparse
from flask_cors import CORS
from kakaokey import KAKAO_KEY 
import requests, os, datetime
from werkzeug.datastructures import FileStorage
from utils.extract_word_2 import extract_txt

app = Flask(__name__)
api = Api(app, version='1.0', title='KB API',
          description='KB REST API 문서')
ns = api.namespace('api/v1/user', description='user 관련 API 목록')
ns2 = api.namespace('api/v1/message', description='message 관련 API 목록')

CORS(app, supports_credentials=True)


logout_parser = ns.parser()
mupload_parser = ns2.parser()
mdetect_parser = ns2.parser()
mshow_parser = ns2.parser()


        


@ns2.route('/upload')
class upload(Resource):

    mupload_parser.add_argument(
        'txt_file', type=FileStorage, required=True, location='files', help="텍스트 파일")
    
    @ns2.expect(mupload_parser)
    @ns2.response(201, '텍스트 파일 업로드 성공')
    @ns2.response(400, 'Bad Request')
    @ns2.response(401, 'INVALID_USER')

    def post(self):
        try :
            args = mupload_parser.parse_args()
            clinet_id = request.headers['client_id']
            
            txt_file = args['txt_file']


            if not os.path.exists('upload'):
                os.makedirs('upload')

            filename = clinet_id + ".txt"  # 서버 디렉토리에 저장하는 과정 (혹시 몰라서 추가) (example을 access_token 로 바꾸기)
            txt_file.save('./upload/{0}'.format(secure_filename(filename)))
            
            result = extract_txt(clinet_id)

            
            
            data = {
                "success": True,
                "message": "텍스트 파일 업로드 성공",
            }
            # 결과 확인 필요 없을 때 주석 풀고 써주기 (result/ 폴더 삭제해주는 기능)
            #shutil.rmtree('./result/')

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
            
            print(message)
            
            # 모델 넘기는 부분 추가하기

            data = {
                "success": True,
                "message": "확인해보고 싶은 메세지 등록 성공",
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