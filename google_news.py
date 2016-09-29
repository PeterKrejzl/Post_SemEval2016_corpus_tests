import gensim
import numpy as np
from scipy import spatial


pretrained_news_corpus = '/Users/peterkrejzl/Disk Google/_PHD/SemEval2016/GoogleNews/GoogleNews-vectors-negative300.bin'
model = gensim.models.word2vec.Word2Vec.load_word2vec_format(pretrained_news_corpus, binary=True)
print('Model loaded')

model.init_sims(replace=True)
print('Memory reduced')

print(model.most_similar('dog'))
print(model.most_similar('paris'))


print(model['dog'])



dog_array = model['dog']
puppy_array = model['puppy']
paris_array = model['paris']


cosine_similarity_dog_puppy = spatial.distance.cosine(dog_array, puppy_array)
cosine_similarity_dog_paris = spatial.distance.cosine(dog_array, paris_array)

print('Dog vs puppy sim = %s' % cosine_similarity_dog_puppy)
print('Dog vs paris sim = %s' % cosine_similarity_dog_paris)





words = ['Let', 'agree', 'that', 'it', 'not', 'ok', 'to', 'kill', 'a', '7lbs', 'baby', 'in', 'the', 'uterus']

for w in words:
    try:
        print('Word = %s, vector = %s' % (w, model[w]))
    except:
        print('Word %s not founds' % w)



#check for how many words in SemEval corpus we have vectors
#ignoring hashtags and so for now
training_data_filename = '/Users/peterkrejzl/Dropbox/PHD/SemEval2016/TrainingData/semeval2016-task6-trainingdata-abortion.txt'

total_words = 0
vectorized_words = 0

with open(training_data_filename, 'r') as input_file:
    for line in input_file:
        split_line = line.split('\t')
        if len(split_line) == 4:
            # print(split_line)
            if split_line[0] != 'ID':
                tweet = split_line[2].strip()

                print(tweet)
                for w in tweet.split():

                    try:
                        vector = model[w]
                        total_words += 1
                        vectorized_words += 1
                    except:
                        total_words += 1



print(total_words)
print(vectorized_words)

#print('Total words = %s, vectorized words = %, percentage = %s' % (total_words, vectorized_words, (float(vectorized_words) / float(total_words))))


