# Copyright 2023 piglake
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ngram
import torch
import torch.nn as nn
from nltk import FreqDist
from nltk import ngrams
#import fasttext.util

cos = nn.CosineSimilarity(dim=1, eps=1e-6)

class score_measure:
    def __init__(self, lang="en"):
        import torch.distributed as dist
        # dist.init_process_group('gloo', init_method='file:///tmp/donot_care', rank=0, world_size=1)
        
        folder = "word2vec-pytorch/weights/cbow_WikiText103"
        #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        device = torch.device("cpu") 

        #model = torch.load(f"./{folder}/model.pt", device).module.eval()#map_location='cuda:0')
        vocab = torch.load(f"./{folder}/vocab.pt")
        
        self.input_embedding, self.output_embedding = torch.load("my_"+lang+"_embedding.pt"), None#model.embeddings, model.linear.weight
        self.vocab = vocab
        self.cos_sim = nn.CosineSimilarity(dim=1, eps=1e-6)
        
    def infer(self, sentence, key_words):
        score = 0
        #print(sentence)
        #print(key_words)
        ids = torch.tensor([ int(self.vocab[i]) for i in sentence.split() ]).unsqueeze(0)
        z = self.input_embedding(ids).mean(axis=1).squeeze()
        #print(z.shape)
        for key_word in key_words:
            index =  self.vocab[key_word]
            z_x = self.input_embedding(torch.tensor(index).unsqueeze(0))
            score += self.cos_sim(z, z_x)
            #score += torch.dot(z, z_x)
            
        return score.cpu().item()


def kmp(pattern, text):
    # Initialize variables
    p_str = pattern
    t_str = text
    lss_arr = []

    # Iterate through the text string
    for i in range(len(t_str)):
        if t_str[i] == p_str[0]:
            lss_arr.append(0)
        else:
            j = 0
            while j < len(lss_arr) and lss_arr[j] + 1 < len(p_str):
                j += 1
            lss_arr[j] += 1

    # Return the longest suffix array
    return lss_arr


def score(key_words, sentence,ft):
    res = 0
    #s = ngram.NGram

    for key_word in key_words.split():
        #res += ngram.NGram.compare(key_word, sentence,N=2)
        #tmp = 0
        #ngram_list = ngrams(key_word, 2) 

        #for gram in ngram_list:
            #gram: tuple
            
            #tmp += sentence.count("".join(gram))
        key_embedding = ft.get_word_vector(key_word)
        #res += 1 if sentence.find(key_word) > 0 else 0

        vector = ft.get_word_vector(sentence)  # 300-dim vector
         
        #print(key_embedding)
    #print(res)
        from numpy import dot
        from numpy.linalg import norm

        cos_sim = dot(key_embedding, vector)/(norm(key_embedding)*norm(vector))
        res += cos_sim
    return res 

def score_2(key_words, sentence,):
    res = 0
    #s = ngram.NGram

    for key_word in key_words.split():
        #res += ngram.NGram.compare(key_word, sentence,N=2)
        #tmp = 0
        #ngram_list = ngrams(key_word, 2) 

        #for gram in ngram_list:
            #gram: tuple
            
            #tmp += sentence.count("".join(gram))

        res += 1 if sentence.find(key_word) > 0 else 0

    return res 

def score_3(key_words, sentence,  measure):
    if sentence.split():
        return measure.infer(sentence, key_words)
    else:
        return -10000 

if __name__ == "__main__":
    ft = fasttext.load_model('cc.en.300.bin')
    #ft = fasttext.load_model('cc.zh.300.bin')
    res = score("hi", \
        " hello, I am Jones", \
            ft = ft
        )
    print(res)
    ft = fasttext.load_model('cc.zh.300.bin')
    res = score("季节", \
        "我最喜欢春天，你呢", \
            ft = ft
        ) 
    print(res)