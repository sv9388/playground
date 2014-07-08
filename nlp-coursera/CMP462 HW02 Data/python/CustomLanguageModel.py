import math
from collections import defaultdict

sb_param = 0.4
class CustomLanguageModel:
  """Unsmoothed Trigrams with stupid backoff(Unsmoothed bigrams+Smoothed Unigram)"""
  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.total = 0
    self.trigrams = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO. Handle sentences with less than three words. 
    for sentence in corpus.corpus:
      self.total+=2
      for i in range(2,len(sentence.data)):
        first = sentence.data[i-2].word
        second = sentence.data[i-1].word
        third = sentence.data[i].word
        self.trigrams[first][second][third]+=1
        self.trigrams[first][second]['<BIGRAM>']+=1
        self.trigrams[first]['<UNIGRAM>']['<UNIGRAM>']+=1
        self.total+=1
      ulti = len(sentence.data)-1
      penulti = ulti-1
      self.trigrams[sentence.data[penulti].word][sentence.data[ulti].word]['<BIGRAM>']+=1
      self.trigrams[sentence.data[ulti].word]['<UNIGRAM>']['<UNIGRAM>']+=1
      self.trigrams[sentence.data[penulti].word]['<UNIGRAM>']['<UNIGRAM>']+=1
    pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i in range(2,len(sentence)):
      one = sentence[i-2]
      two = sentence[i-1]
      three = sentence[i]
      if self.trigrams[one][two][three]>0:
        score+=math.log(self.trigrams[one][two][three])
        score-=math.log(self.trigrams[one][two]['<BIGRAM>'])
        pass
      elif self.trigrams[two][three]['<BIGRAM>']>0:
        score+=math.log(sb_param)
        score+=math.log(self.trigrams[two][three]['<BIGRAM>'])
        score-=math.log(self.trigrams[two]['<UNIGRAM>']['<UNIGRAM>'])
        pass
      else:
        score+=(math.log(sb_param)*2)
        score+=math.log(self.trigrams[three]['<UNIGRAM>']['<UNIGRAM>']+1)
        score-=math.log(self.total*2)
        pass
    return score
