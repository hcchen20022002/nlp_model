#!/usr/bin/python3
# coding=UTF-8

import sys, argparse

def get_pos_taggeer(sentences = []):
    from nltk.tag import StanfordPOSTagger
    result_list = []
    st = StanfordPOSTagger('/home/normanc/NTNU/lab106/create_corpus/stanfordNLP_parser/stanford-postagger-full-2015-12-09/models/english-bidirectional-distsim.tagger',
            '/home/normanc/NTNU/lab106/create_corpus/stanfordNLP_parser/stanford-postagger-full-2015-12-09/stanford-postagger-3.6.0.jar')
    for sen in sentences:
        #
        print(sen)
        #
        result = st.tag(sen.split())
        if output_file:
            for wd in result:
                #
                print(wd)
                #
                string = '{0}/{1} '.format(wd[0], wd[1]) 
                result_list.append(result)
    return result_list

def get_parse(sentences = []):
    import os
    from nltk.parse import stanford
    os.environ['CLASSPATH'] = '/home/normanc/NTNU/lab106/create_corpus/stanfordNLP_parser/stanford-parser-full-2015-12-09/stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = '/home/normanc/NTNU/lab106/create_corpus/stanfordNLP_parser/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'

    stanford_parser = stanford.StanfordParser(model_path='/home/normanc/NTNU/lab106/create_corpus/stanfordNLP_parser/stanford-english-corenlp-2016-01-10-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
    #result_sentences = stanford_parser.raw_parse_sents(sentences)
    result_list = stanford_parser.raw_parse_sents(sentences)
    result_sentences = [ _ for _ in result_list ]

    return result_sentences

def get_ner(sentences = []):
    import os
    from nltk.tag import StanfordNERTagger
    from nltk.tokenize import word_tokenize

    st = StanfordNERTagger('/home/normanc/NTNU/lab106/create_corpus/stanfordNLP_parser/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz',
            '/home/normanc/NTNU/lab106/create_corpus/stanfordNLP_parser/stanford-ner-2015-04-20/stanford-ner.jar',
            encoding='utf-8')
    result_list = []
    for sen in sentences:
        tokenized_sen = word_tokenize(sen)
        result_list.append(st.tag(tokenized_sen))
    return result_list


if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['tagger', 'parser', 'ner'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a ')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a ')
    opt = parser.parse_args(sys.argv[1:])

    sentences_list = []
    with open(opt.Input) as f:
        for line in f:
            sentences_list.append(line.replace('\n', ''))

    if opt.option == 'tagger':
        print(get_pos_taggeer(sentences_list))
    elif opt.option == 'parser':
        break_switch = 0
        results = get_parse(sentences_list)
        for sen in results:
            for i in sen:
                print('list with tag: {0}'.format(i.pos()))
            print('________________________________________')
#        with open(opt.Output, 'w') as output_f:
#            for line in results:
#                for _ in line:
#                    output_f.write(str(_))
    elif opt.option == 'ner':
        print(get_ner(sentences_list))
