# -*- coding: utf-8 -*-
import os
if not os.path.exists('result'):
    os.makedirs('result')

def extract_txt(clinet_id):
    filename = clinet_id + ".txt" 
    source = "./upload/"+filename #input 이미지 경로

    #text = ""
    chat = open(source, encoding="utf-8")
    #추출을 위한 채팅 원본 파일로, 읽기 모드로 가져온다. 'r'값은 기본값이라 생략했다.
    print("chat: ", chat)
    leechat = open("./result/lee_Chats.txt", 'w', encoding="utf-8")
    jangchat = open("./result/jang_Chats.txt", 'w', encoding="utf-8")
    #각 사용자별로 새 텍스트 파일을 생성해준다. 'w' 쓰기모드
    
    mh = "이하영"
    sik = "독서왕"

    with chat as txt :
        lines = txt.readlines()
        
        for line in lines[4:] :
            print(line)
            if '] [' in line :
                if mh in line:
                    print("lee")
                    leechat.write( line.split('] ')[2].replace('이모티콘\n', "").replace("사진\n", "").replace('삭제된 메세지입니다.\n', "").replace('ㅇ', '').replace("샵검색", '') )
                if sik in line:
                    print("jang")
                    jangchat.write( line.split('] ')[2].replace('이모티콘\n', "").replace("사진\n", "").replace('삭제된 메세지입니다.\n', "").replace('ㅇ', '').replace("샵검색", '') )
            
    chat.close()
    leechat.close()
    jangchat.close()