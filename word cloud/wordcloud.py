import pandas as pd
import re
import unidecode
import nltk
import string
from nltk.corpus import stopwords
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
# words that can be considered for removal in pre-processing
add_stopwords = ['s', 'userhandle', 'user', 'u', 'a', 'amp', 'presidential', '2020', 'democratic']


def lemma(tweet):
    # removal of stopwords
    words = [word
             for word in tweet.split()
             if word not in stop_words]

    # print(words)
    tweet_stem = ' '.join(words)

    # removal proposals
    tweet_stem = re.sub(r'[^\w\s]', '', tweet_stem)
    # print(tweet_stem)
    return tweet_stem + " "


def preprocess(tweet):
    # convert to lowercase
    tweet = tweet.lower()

    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet)

    # Convert @username to __USERHANDLE
    tweet = re.sub('@[^\s]+', '', tweet)

    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    # trim
    tweet = tweet.strip('\'"')

    # Repeating words like hellloooo
    repeat_char = re.compile(r"(.)\1{1, }", re.IGNORECASE)
    tweet = repeat_char.sub(r"\1\1", tweet)

    # remove non ascii
    tweet = unidecode.unidecode(tweet)

    # removal of punctuations
    tweet = tweet.translate(str.maketrans(' ', ' ', string.punctuation))
    return tweet


# candidates' csv file to read
filename = ''

# candidate name for word cloud file
candidate_name = ''
words_file = candidate_name + 'words.csv'

data = pd.read_csv(filename, header=None)
d = [lemma(preprocess(tweet)) for tweet in data[1]] # data[column] where column => column containing tweets

# list of all candidates to be removed from the tweets
candidates_names = ["bernie", "berni", "sanders", "sander", "joe", "biden", "elizabeth", "warren", "donald", "trump", "mayor", "pete",
                    "buttigieg", "kamala", "harris", "andrew", "yang", "tulsi", "gabbard"]
str = ''
d = str.join(d)
for i in candidates_names:
    d = d.replace(i, '')

# removal of punctuations
d = re.sub(r'[^\w\s]', '', d)

# Convert string to series
series = pd.Series(d.split())
print(series)
series.to_csv(words_file)


