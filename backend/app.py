# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
# from bson import json, json_util
from flask_restx import Resource, Api, fields, reqparse
from flask_cors import CORS
import os
from werkzeug.datastructures import FileStorage
#from detection import predict
# from torch import nn
# import torch

app = Flask(__name__)
api = Api(app, version='1.0', title='KB API',
          description='KB REST API 문서')
ns = api.namespace('api/v1/message', description='message 관련 API 목록')

CORS(app, supports_credentials=True)

mdetect_parser = ns.parser()

@ns.route('/detect')
class detect(Resource):

    mdetect_parser.add_argument(
        'message', type=str, required=True, location='json', help="메세지")
    
    @ns.expect(mdetect_parser)
    @ns.response(201, '확인해보고 싶은 메세지 등록 성공')
    @ns.response(400, 'Bad Request')
    @ns.response(401, 'INVALID_USER')

    def post(self):
        
        try :
            args = mdetect_parser.parse_args()
            # clinet_id = request.headers['client_id'] 회원가입 기능 추가한다면 넣기
            
            message = args['message']
            
            print("message : ", message)
            
            # 모델 넘기는 부분 추가하기
            #result = predict(message)
            #print("result : ", result)
            
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

# class BERTClassifier(nn.Module):
#     def __init__(self,
#                  bert,
#                  hidden_size = 768,
#                  num_classes=3,   ##클래스 수 조정##
#                  dr_rate=None,
#                  params=None):
#         super(BERTClassifier, self).__init__()
#         self.bert = bert
#         self.dr_rate = dr_rate
                 
#         self.classifier = nn.Linear(hidden_size , num_classes)
#         if dr_rate:
#             self.dropout = nn.Dropout(p=dr_rate)
    
#     def gen_attention_mask(self, token_ids, valid_length):
#         attention_mask = torch.zeros_like(token_ids)
#         for i, v in enumerate(valid_length):
#             attention_mask[i][:v] = 1
#         return attention_mask.float()

#     def forward(self, token_ids, valid_length, segment_ids):
#         attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
#         _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
#         if self.dr_rate:
#             out = self.dropout(pooler)
#         return self.classifier(out)



# app.run(host='0.0.0.0',debug=True)
if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', debug=True)
# gunicorn --bind 0.0.0.0:5000 wsgi:app