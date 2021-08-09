# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, session, Response, render_template
from werkzeug.utils import secure_filename
# from bson import json, json_util
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
    
    def get(self):
        return render_template('login.html')

    def post(self):

        login_user = request.json
        id = login_user['id']

        password = login_user['password']

        result = user.find_one({"id": id})  # user table에서 일치하는 아이디 검색
        if result is None:  # 일치하는 아이디가 없음
            data = {
                "message": "해당 아이디가 없습니다",
            }
            response = jsonify(data)
            response.status_code = 403
            return response

        if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].decode("utf8").encode('utf-8')):
            id = result['id']
            payload = {
                'id': id
            }
            token = jwt.encode(payload, SECRET_KEY, ALGORITHM)  # 토큰 생성(인코딩)
            token = jwt.decode(token, SECRET_KEY, ALGORITHM)  # 토큰 디코팅

            session['id'] = login_user['id']

            data = {
                "success": True,
                "message": "로그인 성공",
                "accessToken": token['id'],
                "user_id": login_user['id']
            }
            response = jsonify(data)
            response.status_code = 201
            response.set_cookie('jwt', token['id'])
            return response

        else:
            data = {
                "message": "비밀번호가 틀렸습니다",
            }
            response = jsonify(data)
            response.status_code = 403
            return response


# app.run(host='0.0.0.0',debug=True)
if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', debug=True)