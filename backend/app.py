# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, session, Response, render_template, redirect
from werkzeug.utils import secure_filename
# from bson import json, json_util
from flask_restx import Resource, Api, fields, reqparse
from flask_cors import CORS
from kakaokey import KAKAO_KEY 

app = Flask(__name__)
api = Api(app, version='1.0', title='KB API',
          description='KB REST API 문서')
ns = api.namespace('api/v1/user', description='user 관련 API 목록')
ns2 = api.namespace('api/v1/message', description='message 관련 API 목록')

CORS(app, supports_credentials=True)

login_parser = ns.parser()
mupload_parser = ns2.parser()
mshow_parser = ns2.parser()



@ns.route('/login')
class login(Resource):

    login_parser.add_argument(
        'id', required=True, location='json', type=str, help='아이디')
    login_parser.add_argument(
        'password', required=True, location='json', type=str, help="비밀번호")

    @ns.expect(login_parser)
    @ns.response(201, '로그인 성공')
    @ns.response(400, 'Bad Request')
    @ns.response(403, "해당 아이디가 없습니다\n 비밀번호가 틀렸습니다")
    
    # def get(self):
    #     return render_template('login.html')

    def post(self):
        client_id = KAKAO_KEY
        redirect_uri = "http://127.0.0.1:5000/account"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
        


# app.run(host='0.0.0.0',debug=True)
if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', debug=True)