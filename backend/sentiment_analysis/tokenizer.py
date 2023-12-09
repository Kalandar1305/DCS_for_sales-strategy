from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import re
from bs4 import BeautifulSoup
import re
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

lemmatizer = WordNetLemmatizer()

# function to remove HTML elements from HTML
def removeHTML(raw_text):
    try:
        clean_HTML = BeautifulSoup(raw_text,features="lxml").get_text() 
        return clean_HTML
    except: 
        return raw_text
    
# function to remove special characters and numbers from the reviews
def remove_special_char(raw_text):
    clean_special_char = re.sub("[^a-zA-Z]", " ", raw_text)  
    return clean_special_char

# function to convert all reviews into lower case
def toLowerCase(raw_text):
    clean_lowerCase = raw_text.lower().split()
    return(" ".join(clean_lowerCase))

def get_wordnet_pos(tag):
    from nltk.corpus import wordnet
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else: 
        return wordnet.NOUN

# function that converts english words to its base form (lemmatize)
def lemmatize(sentance):
    tagged = pos_tag( [i for i in sentance if i])
    lemmatized = []
    for word, tag in tagged:
        lemma = lemmatizer.lemmatize(word, pos = get_wordnet_pos(tag))
        lemmatized.append(lemma)
    return lemmatized

# function to remove stop words from the reviews
def remove_stop_words(raw_text):
    stops = set(stopwords.words("english"))
    words = [w for w in raw_text if not w in stops]
    return words

# function which combines all above operations to a single function
def customTokenizer(text):
    text = removeHTML(text)
    text = remove_special_char(text)
    text = toLowerCase(text)
    tokens = word_tokenize(text)
    tokens = remove_stop_words(tokens)
    tokens = lemmatize(tokens)
    return tokens