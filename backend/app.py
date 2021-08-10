# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, session, Response, render_template, redirect
from werkzeug.utils import secure_filename
# from bson import json, json_util
from flask_restx import Resource, Api, fields, reqparse
from flask_cors import CORS
from kakaokey import KAKAO_KEY 
import requests

app = Flask(__name__)
api = Api(app, version='1.0', title='KB API',
          description='KB REST API 문서')
ns = api.namespace('api/v1/user', description='user 관련 API 목록')
ns2 = api.namespace('api/v1/message', description='message 관련 API 목록')

CORS(app, supports_credentials=True)

login_parser = ns.parser()
logout_parser = ns.parser()
mupload_parser = ns2.parser()
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
class login_token(Resource):

    @ns.expect(login_parser)
    @ns.response(201, '카카오 연결 로그인 성공')
    @ns.response(400, 'Bad Request')
   

    def get(self):
        
    
        try:
            code = request.args["code"]            
            print(code)                        
            client_id = KAKAO_KEY
            redirect_uri = "http://127.0.0.1:5000/api/v1/user/account"
            
            token_request = requests.get(                                        
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            
            token_json = token_request.json()                                    
            print(token_json)
            error = token_json.get("error",None)

            if error is not None :
                data = {
                    "message": "INVALID_CODE"
                }
                response = jsonify(data)
                response.status_code = 400
                return response

            access_token = token_json.get("access_token")                        
            print(access_token)
            data = {
                "message": "SUCCESS_TOKEN",
                "success": True,
                "access_token" : access_token
            }   
            response = jsonify(data)
            response.status_code = 200
            return redirect(
                "http://127.0.0.1:5000/api/v1/user/main"
            )
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

    logout_parser.add_argument(
        'access_token', required=True, location='json', type=str, help='엑세스 토큰')
    

    @ns.expect(logout_parser)
    @ns.response(201, '로그아웃 성공')
    @ns.response(400, 'Bad Request')
    
    
   
    def post(self):
        access_token = request.headers['access_token']

        API_URL = 'https://kapi.kakao.com/v1/user/unlink'
        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        output=requests.post(API_URL, headers=headers).json()
        print(output)
        result=output['id']
        data = {
                    "message" : "SUCCESS_UNLINK",
                    "result" : result
                    
            }
        response = jsonify(data)
        response.status_code = 200
        return response

@ns.route('/main')
class main(Resource):

    def get(self):
        return render_template('main.html')

   
        

# app.run(host='0.0.0.0',debug=True)
if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', debug=True)