#!/usr/bin/python3
# coding=UTF-8

import sys, argparse

def get_post_taggeer(sentences = []):
    from nltk.tag import StanfordPOSTagger
    result_list = []
    st = StanfordPOSTagger('stanfordNLP_parser/stanford-postagger-full-2015-12-09/models/english-bidirectional-distsim.tagger',
            'stanfordNLP_parser/stanford-postagger-full-2015-12-09/stanford-postagger-3.6.0.jar')
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
    os.environ['CLASSPATH'] = 'stanfordNLP_parser/stanford-parser-full-2015-12-09/stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = 'stanfordNLP_parser/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'

    stanford_parser = stanford.StanfordParser(model_path='stanfordNLP_parser/stanford-english-corenlp-2016-01-10-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
    #result_sentences = stanford_parser.raw_parse_sents(sentences)
    result_list = stanford_parser.raw_parse_sents(sentences)
    result_sentences = [ _ for _ in result_list ]

    return result_sentences

if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['tagger', 'parser'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a ')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a ')
    opt = parser.parse_args(sys.argv[1:])

    sentences_list = []
    with open(opt.Input) as f:
        for line in f:
            sentences_list.append(line.replace('\n', ''))

    if opt.option == 'tagger':
        print(get_post_taggeer(sentences_list))
    elif opt.option == 'parser':
        break_switch = 0
        results = get_parse(sentences_list)
        for sen in results:
            for i in sen:
                for h in range(1, i.height()):
                    for s_tree in i.subtrees(lambda i: i.height() == h):
                        if "Parkinson" in str(s_tree)\
                                and 'subjects' in str(s_tree):
                            print('Height: {0}'.format(h))
                            print('tree: {0}'.format(s_tree))
                            print('list with tag: {0}'.format(s_tree.pos()))
                            break_switch = 1
                            break
                    if break_switch == 1:
                        break_switch = 0
                        break

            print('________________________________________')
#        with open(opt.Output, 'w') as output_f:
#            for line in results:
#                for _ in line:
#                    output_f.write(str(_))
