import math
from collections import defaultdict

stupid_backoff_param = 0.8

class StupidBackoffLanguageModel:
  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.ubigrams = defaultdict(lambda:defaultdict(lambda:0))
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      """for start token"""
      self.total+=1
      for i in range(1,len(sentence.data)):
        prev = sentence.data[i-1].word
        data = sentence.data[i].word
        self.ubigrams[prev][data]+=1
        self.ubigrams[prev]['<UNIGRAM>']+=1
        self.total+=1
      self.ubigrams[sentence.data[len(sentence.data)-1]]['<UNIGRAM>']
    pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i  in range(1,len(sentence)):
      token = sentence[i]
      prev = sentence[i-1]
      """Bigram avl?"""
      if self.ubigrams[prev][token]>0:
        score+=math.log(self.ubigrams[prev][token])
        score-=math.log(self.ubigrams[prev]['<UNIGRAM>'])
      else:
        """Smoothen unigram"""
        score+=math.log(stupid_backoff_param)
        score+=math.log(self.ubigrams[token]['<UNIGRAM>']+1)
        score-=math.log(self.total*2) 
    return score
