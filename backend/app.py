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



@ns.route('/login')
class login(Resource):

    def get(self):
        return render_template('login.html')

    def post(self):
        client_id = KAKAO_KEY
        redirect_uri = "http://127.0.0.1:5000/api/v1/user/account"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
    

@ns.route('/account')
class account(Resource):

    
    @ns.response(201, '카카오 연결 로그인 성공')
    @ns.response(400, 'Bad Request')

    def get(self):
    
        try:
            
            code = request.args["code"]            
                                
            client_id = KAKAO_KEY
            redirect_uri = "http://127.0.0.1:5000/api/v1/user/account"
            
            token_request = requests.get(                                        
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )

            token_json = token_request.json()                                    

            error = token_json.get("error",None)

            if error is not None :
                data = {
                    "message": "INVALID_CODE"
                }
                response = jsonify(data)
                response.status_code = 400
                return response

            access_token = token_json.get("access_token")  

            data = {
                "message": "SUCCESS_TOKEN",
                "success": True,
                "access_token" : access_token,
                "client_id" : client_id
            }   

            response = jsonify(data)
            response.status_code = 201
            return response

        except KeyError:
            data = {
                    "message": "INVALID_TOKEN"
            }
            response = jsonify(data)
            response.status_code = 400
            return response
           

        except NameError:
            data = {
                    "message": "INVALID_TOKEN"
            }
            response = jsonify(data)
            response.status_code = 400
            return response
        

@ns.route('/logout')
class logout(Resource):

    @ns.response(201, '로그아웃 성공')
    @ns.response(400, 'Bad Request')
    
    
    def post(self):
        access_token = request.headers['access_token']
        client_id = KAKAO_KEY

        API_URL = 'https://kapi.kakao.com/v1/user/unlink'
        Logout_Redirect_URI ="https://naver.com"
        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        output=requests.post(API_URL, headers=headers).json()
        logout_request = requests.get(                                        
                f"https://kauth.kakao.com/oauth/logout?client_id={client_id}&logout_redirect_uri={Logout_Redirect_URI}"
            )
        
    
      
        id=output['id']
        data = {
                    "message" : "SUCCESS_UNLINK",
                    "id" : id
                    
            }
        response = jsonify(data)
        response.status_code = 201
        return response


@ns.route('/main')
class main(Resource):

    def get(self):
        return render_template('main.html')


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
            #print(result)
            
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
            clinet_id = request.headers['client_id']
            
            message = args['message']
            
            print(message)

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