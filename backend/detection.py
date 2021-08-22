# import torch
# from torch import nn
# import torch.nn.functional as F
# import torch.optim as optim
# from torch.utils.data import Dataset, DataLoader
# import gluonnlp as nlp
# import numpy as np
# from tqdm import tqdm, tqdm_notebook
# import pandas as pd

# #kobert
# from kobert.utils import get_tokenizer
# from kobert.pytorch_kobert import get_pytorch_kobert_model

# #transformers
# from transformers import AdamW
# from transformers.optimization import get_cosine_schedule_with_warmup

# #GPU 사용
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# #BERT 모델, Vocabulary 불러오기
# bertmodel, vocab = get_pytorch_kobert_model()

# #1.경로 지정
# chatbot_data = pd.read_excel('3_1_class_kobert_data.xlsx')

# data_list = []
# for q, label in zip(chatbot_data['text'], chatbot_data['label'])  :
#     data = []
#     data.append(q)
#     data.append(str(label))

#     data_list.append(data)

# #train & test 데이터로 나누기
# from sklearn.model_selection import train_test_split
                                                         
# dataset_train, dataset_test = train_test_split(data_list, test_size=0.24, random_state=0)

# class BERTDataset(Dataset):
#     def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
#                  pad, pair):
#         transform = nlp.data.BERTSentenceTransform(
#             bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

#         self.sentences = [transform([i[sent_idx]]) for i in dataset]
#         self.labels = [np.int32(i[label_idx]) for i in dataset]

#     def __getitem__(self, i):
#         return (self.sentences[i] + (self.labels[i], ))

#     def __len__(self):
#         return (len(self.labels))

# # Setting parameters
# max_len = 64
# batch_size = 64
# warmup_ratio = 0.1
# num_epochs = 15
# max_grad_norm = 1
# log_interval = 200
# learning_rate =  5e-5

# #토큰화
# tokenizer = get_tokenizer()
# tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

# data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)
# data_test = BERTDataset(dataset_test, 0, 1, tok, max_len, True, False)

# train_dataloader = torch.utils.data.DataLoader(data_train, batch_size=batch_size, num_workers=2)
# test_dataloader = torch.utils.data.DataLoader(data_test, batch_size=batch_size, num_workers=2)

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

# #BERT 모델 불러오기
# model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)

# #optimizer와 schedule 설정
# no_decay = ['bias', 'LayerNorm.weight']
# optimizer_grouped_parameters = [
#     {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
#     {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
# ]

# optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate)
# loss_fn = nn.CrossEntropyLoss()

# t_total = len(train_dataloader) * num_epochs
# warmup_step = int(t_total * warmup_ratio)

# scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)

# #정확도 측정을 위한 함수 정의
# def calc_accuracy(X,Y):
#     max_vals, max_indices = torch.max(X, 1)
#     train_acc = (max_indices == Y).sum().data.cpu().numpy()/max_indices.size()[0]
#     return train_acc
    
# train_dataloader

# #2. 경로 지정
# model_path='3_1_class_kobert_model'

# # torch.save(model, model_path)
# # # model = torch.load(model_path)
# # # model.eval()
# print("model save")

# #토큰화
# tokenizer = get_tokenizer()
# tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

# def predict(predict_sentence):
#     model_save = torch.load(model_path, map_location=device)
#     model_save.eval()
#     data = [predict_sentence, '0']
#     dataset_another = [data]

#     another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
#     test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
    
#     model_save.eval()

#     for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
#         token_ids = token_ids.long().to(device)
#         segment_ids = segment_ids.long().to(device)

#         valid_length= valid_length
#         label = label.long().to(device)

#         out = model_save(token_ids, valid_length, segment_ids)


#         test_eval=[]
#         for i in out:
#             logits=i
#             logits = logits.detach().cpu().numpy()
           
#             if np.argmax(logits) == 0:
#                 test_eval.append("지인 사칭")
#             elif np.argmax(logits) == 1:
#                 test_eval.append("기관 사칭")
#             elif np.argmax(logits) == 2:
#                 test_eval.append("정상 말투")
               
               
#         return test_eval[0]
#         # print(">> 입력하신 내용에서 " + test_eval[0] + " 느껴집니다.")