import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


corpus_filename = '/Users/peterkrejzl/Disk Google/_PHD/SemEval2016/CzClassifierSourceCode/Idnes/noentity_out.txt'
model_name = 'Idnes_w2v.model'



sentences = [['first', 'sentence'], ['second', 'sentence']]
sentences = []

#load sentences into sentences []

with open (corpus_filename, 'r') as input_filename:
    for line in input_filename:
        sentences.append(line.strip().split())
        sentences.append(line.strip())



print(sentences[0:5])






logging.log(logging.INFO, 'start building w2v model')

# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, min_count=1, size=300, workers=8, iter=15)
logging.log(logging.INFO, 'W2V model built')



model.save(model_name)
logging.log(logging.INFO, 'model saved to ' + model_name)


new_model = gensim.models.Word2Vec.load(model_name)



print('done')


