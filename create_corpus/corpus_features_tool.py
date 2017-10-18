#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json, time, re

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
        if 1 == _['polarity']:
            positive_count = positive_count + 1
        elif 0 == _['polarity']:
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
    item_pos_dir = {}
    total = 0
    positive_count = 0
    negative_count = 0
    if 'all' == f_type:
        for sen in contents:
            if drug not in itme_pos_dir:
                item_pos_dir[drug] = _get_item_pos(drug)
            if disease not in itme_pos_dir:
                item_pos_dir[disease] = _get_item_pos(disease)
            word_features = _get_word_feature(item_pos_dir[drug],
                    item_pos_dir[disease], sen['pos_tree'])

            feature = '{0} 1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6} 7:{7} 8:{8} 9:{9} 10:{10} '.format(
                    sen['polarity'],
                    sen['pos_tree_height'],
                    len( sen['tree_sentence']),
                    word_features['first_item_type'],
                    word_features['closest_verb'],
                    word_features['closest_verb_distance'],
                    word_features['closest_noun'],
                    word_features['closest_noun_distance'],
                    len(word_features['reverse_wd_location_liste']),
                    word_features['closest_reverse_wd_distance'],
                    word_features['symbol_count'])
            # add words ascii code feature
            feature = feature + '1001:{0} '.format(len(word_features['verb_list']))
            verb_num = 1002
            for verb in verb_list:
                feature = feature + '{0}:{1} '.format(verb_num, verb[0])
                verb_num = verb_num + 1
            feature = feature + '2001:{0} '.format(len(word_features['noun_list']))
            noun_num = 2002
            for noun in noun_list:
                feature = feature + '{0}:{1} '.format(noun_num, noun[0])
                verb_num = noun_num + 1

            feature_file = '{0}_{1}'.format(sen['disease'], sen['drug'])
            with open('all_type_' + feature_file, 'a') as f:
                f.write(feature)
                f.write('\n')

            disease_drug_pair_dir[feature_file] = 1 if feature_file not in disease_drug_pair_dir\
                    else disease_drug_pair_dir[feature_file] + 1

    return disease_drug_pair_dir

# pos_tree example
# [('the', 'DT'), ('pattern', 'NN'), ('of', 'IN'), ('hypertonus', 'NNS'), ('in', 'IN'), ('athetosis', 'NNS'), (',', ','), ('Parkinson', 'NNP'), ("'s", 'POS'), ('disease', 'NN'), (',', ','), ('Fluticasone', 'NNP'), ('propionate', 'NNP'), (',', ','), ('spasticity', 'RB'), (',', ','), ('and', 'CC'), ('activated', 'VBN'), ('normal', 'JJ'), ('subjects', 'NNS')]
def _get_word_feature(drug_pos = [], disease_pos = [], pos_tree = []):
    reverse_word_database = ['no', 'not', 'non', "n't"]
    symbol_count = 0
    drug_index = 0
    disease_index = 0
    # drug first = 1, disease first = 2, default is drug first
    first_item_type = 1
    verb_list = []
    noun_list = []
    reverse_wd_location_list = []
    
    # get each needed words location and ASCII code
    count = 0
    countinue_flag = 0
    for wd in pos_tree:
        # skip second word if drug or disease have two or more words
        if 0 != continue_flag:
            countinue_flag = continue_flag - 1
            continue
        count = count + 1
        if wd[0] == drug_pos[0][0]:
            continue_flag = len(drug_pos) - 1
            drug_index = count
        elif wd[0] == disease_pos[0][0]:
            continue_flag = len(disease_pos) - 1
            disease_index = count
        elif wd[0] in reverse_word_database:
            reverse_wd_location_list.append([ _get_ASCII(wd[0]), count])
        elif re.match(wd[1], '^V'):
            verb_list.append([ _get_ASCII(wd[0]), count])
        elif re.match(wd[1], '^N'):
            noun_list.append([ _get_ASCII(wd[0]), count])
        elif wd[0] == wd[1]:
            symbol_count = symbol_count + 1
    # coounting words relation by distance
    if 0 == drug_index or 0 == disease:
        return 'Cannot find item: '.format(pos_tree)
    if drug_index > disease_index:
        first_item_type = first_item_type + 1
    itme_index = [drug_index, disease_index]
    # get the closest words
    first_itme_index = itme_index[first_item_type - 1]
    closest_verb = _get_closest_distance(first_itme_index, verb_list)
    closest_noun = _get_closest_distance(first_itme_index, noun_list)
    closest_reverse_wd = _get_closest_distance(first_itme_index, reverse_wd_location_list)

    word_features = {
            'first_item_type': first_item_type,
            'closest_verb': closest_verb[0],
            'closest_verb_distance': closest_verb[1],
            'closest_noun': closest_noun[0],
            'closest_noun_distance': closest_noun[1],
            'reverse_wd_location_list': reverse_wd_location_list,
            'closest_reverse_wd_distance': closest_reverse_wd[1],
            'symbol_count': symbol_count,
            'verb_list': verb_list,
            'noun_list': noun_list}
    return word_features

def _get_item_pos(item = ''):
    import stanford_corenlp_tool as stanford_tool
    tree = stanford_tool.get_parse([item])
    for term_tree in tree:
        for term in term_tree:
            pos_list = term.pos()
    return pos_list

def _get_ASCII(string = ''):
    ASCII_value = 0
    for index in range(0, 20):
        if len(string) > (index + 1):
            ASCII_value = ASCII_value + \
                    ord(string[index])*(10**(3*(20-index-1)))
    return ASCII_value

def _get_closest_word(target = int(), word_list = []):
    if 0 == len(word_list):
        return [0, 9999999]
    else:
        location_list = [ _[1] for _ in word_list]
        shortest_distance = min([ abs(_ - target) for _ in location_list])
        return [ word_list[location_list.index(shortest_distance)][0]
                , shortest_distance ]

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
