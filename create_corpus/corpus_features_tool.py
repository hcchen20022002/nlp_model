#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json, time

def get_info(contents = []):
    print('quantity of data: {0}'.format(len(contents)))
    positive_count = 0
    negative_count = 0
    for _ in contents:
#        print('Disease: {0}'.format(_['disease']))
#        print('Drug: {0}'.format(_['drug']))
#        print('Polarity: {0}'.format(_['polarity']))
#        print('Original Sentens: {0}'.format(_['orig_sen']))
#        print('__________________________________________________')
        if _['polarity'] == 1:
            positive_count = positive_count + 1
        elif _['polarity'] == 0:
            negative_count = negative_count + 1
            if _['drug'] == 'gefitinib':
                print(_['orig_sen'])
                print(_['drug'])
                print(_['disease'])
                print('_____________________________________________________')
    print('Positive value: {0}'.format(positive_count))
    print('negative value: {0}'.format(negative_count))
    return True

def create_feature(contents = [], f_type = 'all'):
    disease_drug_pair_dir = {}
    total = 0
    positive_count = 0
    negative_count = 0
    if 'all' == f_type:
        for _ in contents:
            word_info = _get_word_feature(_['drug'], _['disease'], _['pos_tree'])
            feature = '{0} 1:{1} 2:{2}'.format(
                    _['polarity'], _['pos_tree_height'],
                    len( _['tree_sentence']))
            feature_file = '{0}_{1}'.format(_['disease'], _['drug'])
            with open('all_type_' + feature_file, 'a') as f:
                f.write(feature)
                f.write('\n')

            disease_drug_pair_dir[feature_file] = 1 if feature_file not in disease_drug_pair_dir\
                    else disease_drug_pair_dir[feature_file] + 1

    return disease_drug_pair_dir

# not yet #################################################################################
def _get_word_feature(drug = '', disease = '', pos_tree = []):
    reverse_word_list = ['no', 'not', 'non', "n't"]
    reverse_word_count = 0
    first_reverse_word_distance = 0
    first_verb_distence = 0
    symbol_count = 0
    # drug or disease
    first_item_type = ''

    for wd_info in pos_tree:

# not yet #################################################################################


if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['info', 'create'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a input text')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')
    parser.add_argument('-f', '--feature-type', type=str, default='all', help='provide features you want to create')
    opt = parser.parse_args(sys.argv[1:])

    with open(opt.Input) as json_f:
        contents = json.load(json_f)

    if 'info' == opt.option:
        get_info(contents)
    elif 'create' == opt.option:
        # this option would create feature directly, not depend on output file
        disease_drug_pair_dir = create_feature(contents, opt.feature_type)
        for pair in disease_drug_pair_dir:
            print('{0}: {1}'.format(pair, disease_drug_pair_dir[pair]))
