# coding: utf-8

# import and setup modules we'll be using in this notebook
import logging
import itertools
import numpy as np
import gensim
import json
from html.parser import HTMLParser
import sys
import unicodedata

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


def head(stream, n=10):
    """Convenience fnc: return the first `n` elements of the stream, as plain list."""
    return list(itertools.islice(stream, n))


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def cleantext(dataframe):
    dataframe = dataframe.replace({'\n': '', '\r': '',
                                   '-': '',
                                   '"': '',
                                   r'\\\\': '',
                                   r'\.': '', r"\'": "", r'\|': '', r'\।': '', '/': '', r'\(': '', r'\)': '', r'\,': '',
                                   '\’': "", r"\:": ""}, regex=True)
    return dataframe


# Takes textfile Splits on
def tokenize(text):
    sentence = text.split(".")
    # sentence = re.split("[, ]+",sentence)
    sentences_list = sentence
    tokens = []
    for each in sentences_list:
        word_l = each.replace("\r\n", " ").split(" ")
        word_list = [i for i in word_l if not i == '']
        tokens += [i.strip() for i in word_list if not i.isdigit() and len(i) not in [0, 1, 2, 4, 5, 6]]
    return tokens


tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))


def remove_punctuation(text):
    return text.translate(tbl)


# file_path = "/disk2/workspace/Raj/python_projects/divya_corpus_text/sampleDivyaData/divyaArticleRecord_50"
# file_path = "/disk2/workspace/Raj/python_projects/divya_corpus_text/divya_corpus/divya_corpus.jsonl"
file_path = "/disk2/workspace/Raj/python_projects/divya_corpus_text/divyaTextRecords/divya_latest_records.jsonl"


def iter_corpus(dump_file):
    """Yield each article from the corpus dump, as a `(title, tokens)` 2-tuple.
    expects input format as json line
    sample recod:
    {"storyid":"121358926",
    "content":"તમે તમારી પ્રોફેશનલ લાઇફમાં પ્રગતિ કરવા માગતા હો  સફળતાનાં મનપસંદ મ્યુઝિક સાંભળવું   ચાલવા જવું વગેરે",
    "slno":"4976355"}
    """
    with open(dump_file, 'rU') as f:
        for line in f:
            record = json.loads(line)
            content = record["content"]
            story_id = record["storyid"]
            tokens = tokenize(content)
            if len(tokens) < 30:
                continue
            yield story_id, tokens


# In[46]:


stream = iter_corpus(file_path)
for story_id, tokens in itertools.islice(iter_corpus(file_path), 2):
    print(story_id, tokens[:10])  # print the article title and its first ten tokens

# In[5]:


# Creating a document stream using iter_corpus class
doc_stream = (tokens for _, tokens in iter_corpus(file_path))

# In[6]:


# creating dictionary from a streamed corpus
id2word_gujrati = gensim.corpora.Dictionary(doc_stream)
print(id2word_gujrati)

# In[49]:


print(id2word_gujrati)
print("Saving the entire dictionary before filtering")
id2word_gujrati.save("./model_data/gu_dict_b4Filtering")

# In[7]:


# ignore words that appear in less than 20 documents or more than 10% documents
id2word_gujrati.filter_extremes(no_below=20, no_above=0.1)
print(id2word_gujrati)

# In[25]:


# save the filtered Dictionary
print("Saving the filtered dictionary")
id2word_gujrati.save_as_text("./model_data/divya_dictionary_text")
id2word_gujrati.save("./model_data/divya_dictionary")


# In[27]:


class DivyaCorpus(object):
    def __init__(self, dump_file, dictionary, clip_docs=None):
        """
        Parse the first `clip_docs` Wikipedia documents from file `dump_file`.
        Yield each document in turn, as a list of tokens (unicode strings).

        """
        self.dump_file = dump_file
        self.dictionary = dictionary
        self.clip_docs = clip_docs

    def __iter__(self):
        self.story_ids = []
        for story_id, tokens in itertools.islice(iter_corpus(self.dump_file), self.clip_docs):
            self.story_ids.append(story_id)
            yield self.dictionary.doc2bow(tokens)

    def __len__(self):
        return self.clip_docs



# create a stream of bag-of-words vectors
divya_corpus = DivyaCorpus(file_path, id2word_gujrati)

# In[29]:


# Saving searlised corpus to disk for data consistency
gensim.corpora.MmCorpus.serialize('divya_bow.mm', divya_corpus)

# In[30]:


# loading data from disk
mm_corpus = gensim.corpora.MmCorpus('divya_bow.mm')
dictionary = gensim.corpora.Dictionary('')

# # Load corpus and dictionary

print(mm_corpus)
print("Training the Model")

corpus = gensim.corpora.MmCorpus("./model_data/divya_bow.mm")
dictionary = gensim.corpora.Dictionary.load("./model_data/divya_dictionary")
print(corpus)
print(dictionary)

# In[54]:


gensim.models.LdaModel(corpus, num_topics=10, id2word=dictionary, chunksize=1000000, passes=10)

# In[37]:


lda_model.save("./model_data/lda_model_improved")


