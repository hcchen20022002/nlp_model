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
        if  1 < len(_['polarity']):
            print(_['polarity'])
        for _i in _['polarity']:
#        if 'false' == _['polarity']:
            if 'false' == _i:
                negative_count = negative_count + 1
            else:
                positive_count = positive_count + 1
#        if _['drug'] in ['thalidomide', 'hypertension', 'haemorrhage']:
            print(_['orig_sen'])
            print(_['pos_tree'])
            print(_['drug'])
            print(_['disease'])
            print('_____________________________________________________')
    print('Positive value: {0}'.format(positive_count))
    print('negative value: {0}'.format(negative_count))
    return True

def create_feature(contents = [], f_type = 'all'):
    disease_drug_pair_dir = {}
    item_pos_dir = {}
    if 'all' == f_type:
        for sen in contents:
            print(sen)
            drug = sen['drug']
            disease = sen['disease']
            if drug not in item_pos_dir:
                item_pos_dir[drug] = _get_item_pos(drug)
            if disease not in item_pos_dir:
                item_pos_dir[disease] = _get_item_pos(disease)
            word_features = _get_word_feature(item_pos_dir[drug],
                    item_pos_dir[disease], sen['pos_tree'])

            feature = '{0} 1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6} 7:{7} 8:{8} 9:{9} 10:{10} 11:{11} 12:{12} 13:{13} 14:{14} 15:{15} 16:{16} 17:{17} 18:{18} 19:{19} 20:{20} 21:{21} 22:{22} 23:{23} 24:{24} 25:{25}'.format(
                    sen['polarity'],
                    sen['pos_tree_height'],
                    len( sen['tree_sentence']),
                    word_features['first_item_type'],
                    word_features['disease_index'],
                    word_features['drug_index'],
                    word_features['verb_list'][0][0],
                    word_features['disease_closest_verb_info'][0],
                    word_features['disease_closest_verb_info'][1],
                    word_features['drug_closest_verb_info'][0],
                    word_features['drug_closest_verb_info'][1],
                    word_features['disease_closest_noun_info'][0],
                    word_features['disease_closest_noun_info'][1],
                    word_features['drug_closest_noun_info'][0],
                    word_features['drug_closest_noun_info'][1],
                    word_features['disease_closest_IN_info'][0],
                    word_features['disease_closest_IN_info'][1],
                    word_features['drug_closest_IN_info'][0],
                    word_features['drug_closest_IN_info'][1],
                    word_features['symbol_count'],
                    word_features['NNP_count'],
                    len(word_features['verb_list']),
                    len(word_features['noun_list']),
                    len(word_features['IN_list']),
                    word_features['reverse_wd_count'],
                    sen['orig_sen'].count(' '))


            feature_file = '{0}_{1}'.format(sen['disease'], sen['drug'])
            print(feature)
            print('________________________________________________________')
            with open('all_type_' + feature_file, 'a') as f:
                f.write(feature)
                f.write('\n')

            disease_drug_pair_dir[feature_file] = 1 if feature_file not in disease_drug_pair_dir\
                    else disease_drug_pair_dir[feature_file] + 1

    return disease_drug_pair_dir

# pos_tree example
# [('the', 'DT'), ('pattern', 'NN'), ('of', 'IN'), ('hypertonus', 'NNS'), ('in', 'IN'), ('athetosis', 'NNS'), (',', ','), ('Parkinson', 'NNP'), ("'s", 'POS'), ('disease', 'NN'), (',', ','), ('Fluticasone', 'NNP'), ('propionate', 'NNP'), (',', ','), ('spasticity', 'RB'), (',', ','), ('and', 'CC'), ('activated', 'VBN'), ('normal', 'JJ'), ('subjects', 'NNS')]
def _get_word_feature(drug_pos = [], disease_pos = [], pos_tree = []):
    reverse_word_database = ['no', 'not', "n't", 'none']
    drug_index = 0
    disease_index = 0
    symbol_count = 0
    NNP_count = 0
    # drug first = 1, disease first = 2, default is drug first
    first_item_type = 1
    verb_list = []
    noun_list = []
    IN_list = []
    reverse_wd_location_list = []
    
    # get each needed words location and ASCII code
    count = 0
    continue_flag = 0
    for wd in pos_tree:
        # skip second word if drug or disease have two or more words
        if 0 != continue_flag:
            continue_flag = continue_flag - 1
            continue
        count += 1
        print('{0} / {1}'.format(wd[0], wd[1]))
        # use to for loop to solve if drug or disease have multi words
        # and some sentences didn't get the first word in pos tree
        for drug_word in drug_pos:
            if drug_word[0].lower() in wd[0].lower() and\
                    0 == drug_index:
                drug_index = count
                continue_flag = continue_flag +\
                        (len(drug_pos) - drug_pos.index(drug_word) - 1)

        for disease_word in disease_pos:
            if disease_word[0].lower() in wd[0].lower() and\
                    0 == disease_index:
                disease_index = count
                continue_flag = continue_flag +\
                        (len(disease_pos) - disease_pos.index(disease_word) - 1)

        if 0 != continue_flag :
            continue
        elif wd[0].lower() in reverse_word_database:
            reverse_wd_location_list.append([ _get_ASCII(wd[0]), count])
        elif re.match('^V', wd[1]):
            verb_list.append([ _get_ASCII(wd[0].lower()), count])
        elif re.match('^N', wd[1]):
            if wd[1] in ['NNP', 'NNPS']:
                NNP_count += 1
            else:
                noun_list.append([ _get_ASCII(wd[0].lower()), count])
        elif re.match('IN', wd[1]):
            IN_list.append([ _get_ASCII(wd[0].lower()), count])
        elif wd[0] == wd[1]:
            symbol_count += 1
    # coounting words relation by distance
    print('drug:' + str(drug_index))
    print('disease:' + str(disease_index))
    if 0 == drug_index or 0 == disease_index:
        first_item_type = 9999
    elif drug_index > disease_index:
        first_item_type += 1
    item_index = [drug_index, disease_index]
    print('first item type:' + str(first_item_type))
    # create default element for empty list
    verb_list = [[0,0]] if not verb_list else verb_list
    noun_list = [[0,0]] if not noun_list else noun_list
    IN_list = [[0,0]] if not IN_list else IN_list
    # get the closest words, [ASCII_value, distance]
    first_item_index = item_index[first_item_type - 1]
    drug_closest_verb = _get_closest_word(drug_index, verb_list)
    drug_closest_noun = _get_closest_word(drug_index, noun_list)
    drug_closest_IN = _get_closest_word(drug_index, IN_list)
    disease_closest_verb = _get_closest_word(disease_index, verb_list)
    disease_closest_noun = _get_closest_word(disease_index, noun_list)
    disease_closest_IN = _get_closest_word(disease_index, IN_list)

    word_features = {
            'drug_index': drug_index,
            'disease_index': disease_index,
            'first_item_type': first_item_type,
            'drug_closest_verb_info': drug_closest_verb,
            'drug_closest_noun_info': drug_closest_noun,
            'drug_closest_IN_info': drug_closest_IN,
            'disease_closest_verb_info': disease_closest_verb,
            'disease_closest_noun_info': disease_closest_noun,
            'disease_closest_IN_info': disease_closest_IN,
            'reverse_wd_count': len(reverse_wd_location_list),
            'symbol_count': symbol_count,
            'NNP_count': NNP_count,
            'verb_list': verb_list,
            'noun_list': noun_list,
            'IN_list': IN_list}
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
    word_max_lenght = 10
    for index in range(0, word_max_lenght):
        if len(string) > index:
            # transform words
            word_value = (ord(string[index]) - 96)
                    #*(ord(string[index])%8 + 1)
            ASCII_value = ASCII_value + \
                    word_value*(10**(2*(word_max_lenght-index-1)))
    return ASCII_value

def _get_closest_word(target = int(), word_list = []):
    if 0 == len(word_list):
        return [0, 9999]
    else:
        location_list = [ abs(_[1] - target) for _ in word_list]
        #shortest_distance = min([ abs(_ - target) for _ in location_list])
        shortest_distance = min(location_list)
        return [ word_list[location_list.index(shortest_distance)][0],
                shortest_distance ]

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
