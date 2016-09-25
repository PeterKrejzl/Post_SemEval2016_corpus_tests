import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import scipy.sparse
from sparsesvd import sparsesvd
from pprint import pprint
from sklearn import cluster
from matplotlib import pyplot



FEATURES = 3000
NGRAM_RANGE = (1,1)
FACTORS = 300 #SVD factors
CLUSTERS = 2 #for K-Means
JOBS = 8 #parallel processing

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
training_data_filename = '/Users/peterkrejzl/Dropbox/PHD/SemEval2016/TrainingData/semeval2016-task6-trainingdata-abortion.txt'


'''
semeval2016-task6-trainingdata-atheism.txt
semeval2016-task6-trainingdata-climate.txt
semeval2016-task6-trainingdata-feminism.txt
semeval2016-task6-trainingdata-hillary.txt
semeval2016-task6-trainingdata.txt
'''





'''
input file format


ID	Target	Tweet	Stance
2312	Legalization of Abortion	I really don't understand how some people are Pro-Choice. A life is a life no matter if it's 2 weeks old or 20 years old. #SemST	AGAINST
2313	Legalization of Abortion	Let's agree that it's not ok to kill a 7lbs baby in the uterus @DWStweets #DNC #Clinton2016 @HillaryforIA #ProCompromise #SemST	AGAINST
2314	Legalization of Abortion	@glennbeck I would like to see poll: How many abortion doctors have told a woman "No, an abortion is not required in your case. #SemST	AGAINST
2315	Legalization of Abortion	Democrats are always AGAINST "Personhood" or what they perceive to be legislation to recognize #Personhood. Always. #Colorado #SemST	AGAINST
2316	Legalization of Abortion	@CultureShifting "If you don't draw the line where I've arbitrarily drawn it, you can't draw it anywhere." Nonsense. #SemST	NONE
'''
def load_data_from_file (training_data_filename):
    logging.log(logging.INFO, 'Loading data from file')
    tweets = []
    stances = []

    with open(training_data_filename, 'r') as input_file:
        for line in input_file:
            split_line = line.split('\t')
            if len(split_line) == 4:
                #print(split_line)
                if split_line[0] != 'ID':
                    topic = split_line[1].strip()
                    tweet = split_line[2].strip()
                    stance = split_line[3].strip()

                    #print(tweet)
                    tweets.append(tweet)
                    stances.append(stance)

    logging.log(logging.INFO, 'data loaded from input file')
    return tweets, stances



'''
TODO: stop words remove
'''
def get_tfid(documents, features, ng_range):
    logging.log(logging.INFO, 'Starting TF-IDF vectorizer (features = ' + str(features) + ', ngram_range = ' + str(ng_range) + ')')
    logging.log(logging.INFO, 'First 3 sentences:')
    logging.log(logging.INFO, '\t' + str(documents[0:3]))
    vectorizer = TfidfVectorizer(analyzer='word', preprocessor=None, stop_words=None, max_features=features, ngram_range=ng_range)
    data_features = vectorizer.fit_transform(documents).toarray()
    vocab = vectorizer.get_feature_names()

    logging.log(logging.INFO, 'TF-IDF calculated (vocabulary contains ' + str(len(vocab)) + ' items)')
    logging.log(logging.INFO, 'First 5 items from the vocabulary:')
    logging.log(logging.INFO, '\t' + str(vocab[0:5]))
    logging.log(logging.INFO, 'First X data features:')
    logging.log(logging.INFO, '\t' + str(data_features[0:5]))

    return data_features, vocab



def convert_to_scipy_sparse_csc (data_features):
    return scipy.sparse.csc_matrix(data_features)



def calculate_SVD (sparse_matrix, factors):
    logging.log(logging.INFO, 'Calculating SVD (factors = ' + str(factors) + ')')
    Ut, s, Vt = sparsesvd(sparse_matrix, factors)

    logging.log(logging.INFO, 'SVD Done (Ut dim = ' + str(Ut.shape) + ', s dim = ' + str(s.shape) + ', Vt dim = ' + str(Vt.shape) + ')')
    return Ut, s, Vt



def cluster_data (data, clusters, visualize, jobs):
    kmeans = cluster.KMeans(n_clusters=clusters, n_jobs = jobs)
    kmeans.fit_transform(data)

    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    if visualize == True:
        for i in range(clusters):
            ds = data[np.where(labels==i)]
            logging.log(logging.INFO, 'Cluster ' + str(i) + ' contains ' + str(len(ds)) + ' items')
            pyplot.plot(ds[:,0], ds[:,1], 'o')
            lines = pyplot.plot(centroids[i,0], centroids[i,1], 'kx')
            pyplot.setp(lines, ms=15.0)
            pyplot.setp(lines, mew=2.0)
        pyplot.show()

    return labels, centroids, kmeans








tweets, stances = load_data_from_file(training_data_filename)

data_features, vocab = get_tfid(tweets, FEATURES, NGRAM_RANGE)


sparse_data_features = convert_to_scipy_sparse_csc(data_features)

#just to be sure :)
assert sparse_data_features.shape == data_features.shape
logging.log(logging.INFO, 'Data features dim = ' + str(data_features.shape))

Ut, s, Vt = calculate_SVD(sparse_data_features, FACTORS)


#first cluster data_features
#clusters various data set to visualize

#_,_,_ = cluster_data(data_features, CLUSTERS, True, JOBS)
#_,_,_ = cluster_data(Vt, CLUSTERS, True, JOBS)
_,_,_ = cluster_data(Ut, CLUSTERS, True, JOBS)