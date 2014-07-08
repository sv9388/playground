import math
from collections import defaultdict
class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.bigrams = defaultdict(lambda:defaultdict(lambda:1))
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      self.total+=1
      self.bigrams[sentence.data[0].word]['<UNIGRAM>']+=1
      for i in range(1,len(sentence.data)):
        data = sentence.data[i].word
        prev = sentence.data[i-1].word
        self.bigrams[prev]['<UNIGRAM>'] = self.bigrams[prev]['<UNIGRAM>']+1
        self.bigrams[prev][data]  = self.bigrams[prev][data]+1
        self.total = self.total+1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i in range(1,len(sentence)):
      prev = sentence[i-1]
      token = sentence[i]
      score+=math.log(self.bigrams[prev][token])
      score-=math.log(self.bigrams[prev]['<UNIGRAM>']+self.total-1)
    return score
