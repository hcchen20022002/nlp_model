#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json, time, re

def get_info(contents = []):
    positive_count = 0
    negative_count = 0
    max_re = 0
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
#        if _['drug1'] in ['thalidomide', 'hypertension', 'haemorrhage']:
        print(_['orig_sen'])
        #print(_['pos_tree'])
        print(_['drug1'])
        print(_['drug2'])
        print(_['polarity'])
        #print(_['disease'])
#        print('_____________________________________________________')
    print('quantity of data: {0}'.format(len(contents)))
    print('Positive value: {0}'.format(positive_count))
    print('negative value: {0}'.format(negative_count))
    return True

def create_feature(contents = [], f_type = 'all'):
    drug_pair_dir = {}
    item_pos_dir = {}
    error_list = []
    error_count = 0
    if 'all' == f_type:
        for sen in contents:
            print(sen)
            item1 = sen['re_drug1']
            item2 = sen['re_drug2']
#            if item1 not in sen['tree_sentence']\
#                    or item2 not in sen['tree_sentence']:
#                error_list.append(sen)
#                error_count += 1
#                continue
            word_features = _get_word_feature(item1, item2, sen['pos_tree'])
            # transform polarity to level
            polarity = 'XXXXXXXXX'
            if sen['polarity'] == 'advise':
                polarity = 1
            elif sen['polarity'] == 'effect':
                polarity = 1
            elif sen['polarity'] == 'mechanism':
                polarity = 1
            elif sen['polarity'] == 'int':
                polarity = 1
            elif sen['polarity'] == 'true':
                polarity = 1
            elif sen['polarity'] == 'false':
                polarity = 0

            feature = '{0} 1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6} 7:{7} 8:{8} 9:{9} 10:{10} 11:{11} 12:{12} 13:{13} 14:{14} 15:{15} 16:{16} 17:{17} 18:{18} 19:{19} 20:{20} 21:{21} 22:{22} 23:{23} 24:{24} 25:{25}'.format(
                    polarity,
                    sen['pos_tree_height'],
                    len( sen['tree_sentence']),
                    0, #drug or disease first type, no use in DDI model
                    word_features['item1_index'],
                    word_features['item2_index'],
                    word_features['verb_list'][0][0],
                    word_features['item1_closest_verb_info'][0],
                    word_features['item1_closest_verb_info'][1],
                    word_features['item2_closest_verb_info'][0],
                    word_features['item2_closest_verb_info'][1],
                    word_features['item1_closest_noun_info'][0],
                    word_features['item1_closest_noun_info'][1],
                    word_features['item2_closest_noun_info'][0],
                    word_features['item2_closest_noun_info'][1],
                    word_features['item1_closest_IN_info'][0],
                    word_features['item1_closest_IN_info'][1],
                    word_features['item2_closest_IN_info'][0],
                    word_features['item2_closest_IN_info'][1],
                    word_features['symbol_count'],
                    word_features['NNP_count'],
                    len(word_features['verb_list']),
                    len(word_features['noun_list']),
                    len(word_features['IN_list']),
                    word_features['reverse_wd_count'],
                    sen['orig_sen'].count(' '))


            feature_file = '{0}_type_data_set'.format(sen['polarity'])
            print(feature)
            print('________________________________________________________')
            with open(feature_file, 'a') as f:
                f.write(feature)
                f.write('\n')

            drug_pair_dir[feature_file] = 1 if feature_file not in drug_pair_dir\
                    else drug_pair_dir[feature_file] + 1

#    with open('error_data.json', 'w') as error_json:
#        json.dump(error_list, error_json)
#    print(error_list)
#    print(error_count)
    return drug_pair_dir

# pos_tree example
# [('the', 'DT'), ('pattern', 'NN'), ('of', 'IN'), ('hypertonus', 'NNS'), ('in', 'IN'), ('athetosis', 'NNS'), (',', ','), ('Parkinson', 'NNP'), ("'s", 'POS'), ('disease', 'NN'), (',', ','), ('Fluticasone', 'NNP'), ('propionate', 'NNP'), (',', ','), ('spasticity', 'RB'), (',', ','), ('and', 'CC'), ('activated', 'VBN'), ('normal', 'JJ'), ('subjects', 'NNS')]
def _get_word_feature(item1, item2, pos_tree = []):
    reverse_word_database = ['no', 'not', "n't", 'none']
    item1_index = 0
    item2_index = 0
    symbol_count = 0
    NNP_count = 0
    verb_list = []
    noun_list = []
    IN_list = []
    reverse_wd_location_list = []
    
    # get each needed words location and ASCII code
    count = 0
    for wd in pos_tree:
        count += 1
        print('{0} / {1}'.format(wd[0], wd[1]))

        if item1 in wd[0]:
            item1_index = count
        elif item2 in wd[0]:
            item2_index = count
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
    print('item1:{0}'.format(item1_index))
    print('item2:{0}'.format(item2_index))
    # create default element for empty list
    verb_list = [[0,0]] if not verb_list else verb_list
    noun_list = [[0,0]] if not noun_list else noun_list
    IN_list = [[0,0]] if not IN_list else IN_list
    # get the closest words, [ASCII_value, distance]
    item1_closest_verb = _get_closest_word(item1_index, verb_list)
    item1_closest_noun = _get_closest_word(item1_index, noun_list)
    item1_closest_IN = _get_closest_word(item1_index, IN_list)
    item2_closest_verb = _get_closest_word(item2_index, verb_list)
    item2_closest_noun = _get_closest_word(item2_index, noun_list)
    item2_closest_IN = _get_closest_word(item2_index, IN_list)

    word_features = {
            'item1_index': item1_index,
            'item2_index': item2_index,
            'item1_closest_verb_info': item1_closest_verb,
            'item1_closest_noun_info': item1_closest_noun,
            'item1_closest_IN_info': item1_closest_IN,
            'item2_closest_verb_info': item2_closest_verb,
            'item2_closest_noun_info': item2_closest_noun,
            'item2_closest_IN_info': item2_closest_IN,
            'reverse_wd_count': len(reverse_wd_location_list),
            'symbol_count': symbol_count,
            'NNP_count': NNP_count,
            'verb_list': verb_list,
            'noun_list': noun_list,
            'IN_list': IN_list}
    return word_features

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
        location_list = [ abs(_[1] - target) for _ in word_list ]
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