# Guide on generating:
# https://huggingface.co/blog/how-to-generate
import random
import time
import torch
from torch.multiprocessing import set_start_method
from transformers import GPT2LMHeadModel, GPT2Tokenizer

mock_sentences = [
    'The quick brown fox jumps over the lazy dog.',
    'Today I will stay at home coding, because the weather is bad.',
    'I\'m hungry! Let\'s order some food. This new Italian is very good.',
    'Do you like to go to the soccer match with me today?'
]
def get_mock_sentence():
    return mock_sentences[random.randint(0, len(mock_sentences)-1)].split(' ')

def get_first_sentence(sen):
    marks = ['.', '?', '!']
    for i in range(len(sen)):
        if len(set(sen[i]).intersection(marks)) > 0:
            return sen[:i+1]
    return sen


class Generator:
    def __init__(self):
        self.index = 0
        self.sentence = []
        self.model_loaded = False
        self.device_set = False
        self.model = None
        self.tokenizer = None
        self.device = None
    

    def load_model(self):
        if self.model_loaded:
            return
        print('Started loading the model') 
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        #add the EOS token as PAD token to avoid warnings
        self.model = GPT2LMHeadModel.from_pretrained("gpt2-medium", pad_token_id=self.tokenizer.eos_token_id)
        print('Finished loading')
        self.model_loaded = True
    

    def set_device(self):
        self.load_model()
        if self.device_set:
            return
        self.device = torch.device('cuda')
        self.model = self.model.to(self.device)
        self.device_set = True


    def generate_sentence(self, keywords):
        self.set_device()

        print('Started generating a sentence')
        t1 = time.perf_counter()

        input_ids = self.tokenizer.encode(keywords, return_tensors='pt').to(self.device)
        input_len = len(input_ids[0])

        sample_output = self.model.generate(
            input_ids, 
            do_sample=True,
            min_length=input_len+30, 
            max_length=input_len+50,
            top_p=0.80, # sample only from 80% most likely words
            top_k=50, # in adition set top_k to 50
            num_return_sequences = 1,
        )
        
        out = self.tokenizer.decode(sample_output[0], skip_special_tokens=False).split(' ')
        
        t2 = time.perf_counter()
        time_needed = t2-t1
        print('- ' + str(time_needed) + ' seconds needed for Generating')

        return out, time_needed
    

    def generate_multiple_options(self, pre, amount):
        self.set_device()

        print('- Started generating a sentence')
        t1 = time.perf_counter()

        input_ids = self.tokenizer.encode(pre, return_tensors='pt').to(self.device)
        input_len = len(input_ids[0])
        
        sample_outputs = self.model.generate(
            input_ids, 
            do_sample=True,
            min_length=input_len+5, 
            max_length=input_len+12,
            top_p=0.80, # sample only from 80% most likely words
            top_k=70,
            num_return_sequences = amount
        )

        out=list()
        for sample_output in sample_outputs:
            sample = self.tokenizer.decode(sample_output, skip_special_tokens=False)[len(pre):].split(' ')
            if sample[0] == '':
                sample = sample[1:]
            out.append(get_first_sentence(sample))
        
        t2 = time.perf_counter()
        time_needed = t2-t1
        print('- ' + str(time_needed) + ' seconds needed for Generating')
        
        return out, time_needed
        

    def create_sentence(self, keywords, mock_sentence=False):
        self.sentence = []
        if mock_sentence or keywords == '':
            self.sentence = get_mock_sentence()
        else:
            self.sentence = self.generate_sentence(keywords)[0]
        return self.sentence
        
        
    def getAt(self, i):
        if i == -1:
            return ''
        if i >= len(self.sentence):
            return '\\eof'
        else:
            return self.sentence[i]



def test1():
    g = Generator()
    answer = 'y'
    while answer == 'y':
        g.create_sentence('I was playing with my dog, when')
        for i in range(-1, 10):
            print(g.getAt(i))
        
        answer = input('You want to try again? (y)(n) ')

def test2():
    g = Generator()
    g.load_model()
    answer = ''
    pre = 'I was playing with my dog'
    while not answer == 'exit':
        print(pre)
        sentences = g.generate_multiple_options(pre, 3)
        print('----- Choose:')
        for i, sen in enumerate(sentences):
            print('['+ str(i) + '] ', sen)
        index = int(input())
        for w in sentences[index]:
            pre += ' ' + w

if __name__ == "__main__":
    test2()
