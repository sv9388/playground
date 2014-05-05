import sys
import os
import re
import pprint

"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

first_part = '([\.\w\d\-\[\]\(\)]+)'

at_prefix = '[\s\(\[\(\)\{%20]+'
at_suffix = '[\s\)\]\(\)\}%20]+'  
at = "("+"|".join(['at','where','in','@'])+")"
at_clause = at_prefix+at+at_suffix

dot_prefix = '[\s\(\[\{]+'
dot = "("+"|".join(['dot','dt','.','dom'])+")"
dot_suffix = '[\s\)\]\}]+'
dot_clause = dot_prefix+dot+dot_suffix

domain_part="([\w\d\+-]+\.)+"
"""Used after replacement"""

top_domain = "("+"|".join(['org','edu','com'])+")"

email_regex = first_part+"\s?@\s?"+domain_part+top_domain

phone_regex2 = "\+{0,1}[\-\(\)]*\d*[\-\(\)]*(\d{3})[\-\(\)]*(\d{3})[\-\(\)]*(\d{4})[\-\(\)]*"

replace_map = {'&thinsp;':' ','&ldquo;':'','&rdquo;':'','\\x08':' ','&#64;':'@','&#x40;':'@','%40':'@','%20':'.','&#46;':'.','&#x2e;':'.','%2e':'.',';':'.'}



def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    emails = set()
    phones = set()

    skip = False    
    for line in f:
        if "<head>" in line.lower():
            skip = True
        if "</head>" in line.lower():
            skip = False
        if not skip:
            """Remove HTML features"""
            for key in replace_map.keys():
                line = re.sub(key,replace_map[key],line)
            line = strip_tags(line)
            line = line.strip().lower()
            
            emails = a_million_dollar_recipients(line)
            phones = hdfc_call_receivers(line)            
            for email in emails:
                res.append((name,'e',email))
            for phone in phones:
                res.append((name,'p',phone))
    return res

def hdfc_call_receivers(line):
    phones = set()
    line = re.sub('\s+','',line)
    if line.endswith('.') is False:
        matches = re.findall(phone_regex2,line)
        for match in matches:
            phones.add('%s-%s-%s' % match)
    return phones

def a_million_dollar_recipients(line):
    emails = set()
    """Email parsing"""
    email = line
    email = re.sub('\s+',' ',email)
    email = re.sub('\s+.*followed by\s+"{0,1}','',email)
    email = re.sub('\-*(\w{1})\-*','\g<1>',email)
    email = re.sub(at_clause,'@',email)
    email = re.sub(dot_clause,'.',email)
    matches = re.search(email_regex,email)
    if matches is not None:
        emails.add(matches.group(0))
    elif "@" in email:
        """pal case"""
    return emails

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) == 1):
        main('../data/dev', '../data/devGOLD')
    elif (len(sys.argv) == 3):
        main(sys.argv[1],sys.argv[2])
    else:
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
