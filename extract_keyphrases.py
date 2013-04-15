import os
import sys
import text_reading.twenty_newsgroups
import nltk

STOP_LIST_ENG = nltk.corpus.stopwords.words('russian')
GOOD_POSES = set(['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS'])

def lower(in_sentence):
    return [word.lower() for word in in_sentence]

def stop(in_sentence):
    return [word for word in in_sentence if word not in STOP_LIST_ENG]

def pos_filter(in_sentence, in_good_poses):
    return [token[0] for token in nltk.pos_tag(in_sentence) if token[1] in in_good_poses]

def load_text_pipeline(in_file_name):
    sentences = text_reading.twenty_newsgroups.load_text(in_file_name)
    result_sentences = []
    for sentence in sentences:
        filtered_sentence = lower(stop(pos_filter(sentence, GOOD_POSES)))
        if len(filtered_sentence):
            result_sentences.append(filtered_sentence)
    return result_sentences

def process_text(in_text_root):
    loaded_texts = {}
    for root, dirs, files in os.walk(in_text_root, followlinks=True):
        for file_name in files:
            full_file_name = os.path.join(root, file_name)
            loaded_texts[full_file_name] = load_text_pipeline(full_file_name)
            print full_file_name
            print loaded_texts[full_file_name]



if __name__ == '__main__':
    if len(sys.argv) < 2:
        # now only for 20newsgroups
        print 'Usage: extract_keyphrases.py <texts root>'
        sys.exit(0)
    process_text(sys.argv[1])