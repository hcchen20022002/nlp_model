#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json

class InputText(object):
    def __init__(self, input_file):
        self.data = self.get_data(input_file)
    def get_data(self, input_file):
        import xml.etree.ElementTree as xmlET
        check_repeat_sentences_list = []
        sentences_list = []
        tree = xmlET.parse(input_file)
        xml_root = tree.getroot()
        polarity_dict = {}
        for child in xml_root:
            entity_dict = {}
            for grandchild in child:
                if 'entity' == grandchild.tag:
                    entity_dict[grandchild.attrib['id']] = grandchild.attrib['text']
                elif 'pair' == grandchild.tag:
                    drug_pair = [ entity_dict[grandchild.attrib['e1']],
                            entity_dict[grandchild.attrib['e2']]]
                    #drug_pair.sort()
                    pair_info = {'orig_sen':child.attrib['text'],
                            'drug1': drug_pair[0],
                            'drug2': drug_pair[1]}
                    polarity = grandchild.attrib['ddi']\
                            if 'type' not in grandchild.attrib\
                            else grandchild.attrib['type']
                    if polarity in polarity_dict:
                        polarity_dict[polarity] += 1
                    else:
                        polarity_dict[polarity] = 1
                    if pair_info not in check_repeat_sentences_list:
                        check_repeat_sentences_list.append(dict(pair_info))
                        pair_info['polarity'] = [polarity]
                        sentences_list.append(dict(pair_info))
                    else:
                        sentences_list[
                                check_repeat_sentences_list.index(
                                    pair_info)]['polarity'].append(polarity)
        print(polarity_dict)
        return sentences_list

def get_parsing_tree(sentences_list = []):
    import re, time
    import stanford_corenlp_tool as stanford_tool

    sentences_list_with_tree = []
    error_dict = {
            'lose_item':[],
            'polarity_error':[],
            'decode_error':[],
            'cannot_find_item':[]}
    for _ in range(0, len(sentences_list)):
        sen_info = sentences_list.pop()
        item1 = sen_info['drug1']
        item2 = sen_info['drug2']
        # [0][0] at the end is because get_parse() would return a list
        # this list only have 1 element by which we input only 1 too
        if re.findall(u'[\u4e00-\u9fff]+', sen_info['orig_sen']):
            print('Have chinese!')
            continue

        item_pair_list = []
        if item1 == item2:
            sentence_with_item_label, item_list = _label_orig_sentence_by_items(
                    sen_info['orig_sen'], [item1])
            # because of pop would do from the end
            #item_list[0].reverse()
            for _ in range(0, len(item_list[0])):
                if item_list[0][(_+1):]:
                    item_pair_list.append([item_list[0][_], item_list[0][(_+1):]])
        else: 
            sentence_with_item_label, item_list = _label_orig_sentence_by_items(
                    sen_info['orig_sen'], [item1,item2])
            for _ in item_list[0]:
                item_pair_list.append([ _, item_list[1]])

        if 1 > len(item_pair_list):
            error_dict['lose_item'].append(sen_info)
            print(sen_info)
            print(item_pair_list)
            print('lose item1 -----------------------------------------------------')
            continue

        continue_switch = False
        for item_pair in item_pair_list:
            if not item_pair[0] or not item_pair[1]:
                error_dict['lose_item'].append(sen_info)
                print(sen_info)
                print(item_pair_list)
                print('lose item2 -----------------------------------------------------')
                continue_switch = True
                break
        if continue_switch:
            continue

        polarity_list = list(sen_info['polarity'])
        if len(item_pair_list)*len(item_pair_list[0][1]) < len(polarity_list):
            error_dict['polarity_error'].append(sen_info)
            print(sen_info)
            print(item_pair_list)
            print('polarity error -----------------------------------------------------')
            continue

        try:
            orig_tree = list(stanford_tool.get_parse(
                    [sentence_with_item_label])[0])
        except UnicodeDecodeError:
            error_dict['decode_error'].append(sen_info)
            print(sen_info)
            print('decode error -----------------------------------------------------')
            continue

        item1_index, item2_index = 0, 0
        print(polarity_list)
        for pair_polarity in polarity_list:
            re_item1, re_item2 = 'NORMAN$', '!CAROLINE'
            check_data_correct, break_switch = 0, 0
            try:
                # item1, 2 have to be in right order in sentence
                while not re.search('{0}.*{1}'.format(re_item1, re_item2),
                        sentence_with_item_label):

                    if item2_index > len(item_pair_list[item1_index][1]) - 1:
                        item1_index += 1
                        item2_index = 0
                    if item1_index > len(item_pair_list) - 1:
                        break_switch = 1
                        break
                    re_item1 = item_pair_list[item1_index][0]
                    re_item2 = item_pair_list[item1_index][1][item2_index]
                    item2_index += 1

                if break_switch == 1:
                    break_switch = 0
                    break
            except IndexError:
                print('item index out of item list')
                print(sen_info)
                print(item1_index)
                print(item2_index)
                print(item_pair_list)
                print(sentence_with_item_label)
                exit()
            # TODO work around for polarity error
            #re_item1 = item_pair_list[item1_index][0]
            #re_item2 = item_pair_list[item1_index][1][item2_index]
            # TODO work around for polarity error
            print(pair_polarity)
            for h in range(0, orig_tree[0].height()):
                for s_tree in orig_tree[0].subtrees(lambda i: i.height() == h):
                    # unified string format for keywords and tree
                    subtree_str = _leaves_list_to_sentence(list(s_tree.leaves()))
                    item1_in_tree_number = subtree_str.count(re_item1)
                    item2_in_tree_number = subtree_str.count(re_item2)
                    # first subtree have every items
                    new_sen = dict(sen_info)
                    if item1_in_tree_number >= 1\
                            and item2_in_tree_number >= 1:
                        new_sen['pos_tree'] = s_tree.pos()
                        new_sen['pos_tree_height'] = h
                        new_sen['tree_sentence'] = s_tree.leaves()
                        new_sen['orig_sen'] = sentence_with_item_label
                        new_sen['re_drug1'] = re_item1
                        new_sen['re_drug2'] = re_item2
                        new_sen['polarity'] = pair_polarity
                        print(new_sen['polarity'])
                        sentences_list_with_tree.append(new_sen)
                        #print(sen_info)
                        #print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        print('Datas already done: {0}'.format(len(sentences_list_with_tree)))
                        check_data_correct = 1
                        break_switch = 1
                        break
                if break_switch == 1:
                    break_switch = 0
                    break

        if not check_data_correct:
            error_dict['cannot_find_item'].append(sen_info)
            print(sen_info)
            print(item_pair_list)
            print(sentence_with_item_label)
            print('cannot find item -----------------------------------------------------')

    with open('error_data.json' + str(time.clock()), 'w') as error_json:
        json.dump(error_dict, error_json)
    for error in error_dict:
        print('{0} datas: {1}'.format(error, len(error_dict[error])))
    return sentences_list_with_tree

def _unified_string(Input = str()):
    import re
    output_list = []
    string = ''
    for _ in Input:
        if _ in [ ' ', "'"] :
            output_list.append(string)
            string = ''
        if ' ' != _ :
            string = string + _.lower()
    output_list.append(string)
    return output_list

def _leaves_list_to_sentence(leaves_list = []):
    return ' '.join(leaves_list)

def _label_orig_sentence_by_items(sen = '', item_list = []):
    import re
    # need a mapping dict, because item transform need to do in order by item string's lenght
    # but label set list need to in order by item_list
    no_spec_char_item_list = []
    copy_item_list = list(item_list)
    copy_item_list.sort(key = len)
    copy_item_list.reverse()
#    replace_item_list = ['itemA', 'itemB', 'itemC', 'itemD']
    for i in range(0, len(copy_item_list)):
        # use tag N to replace specoal word, if just remove, item1 and item2 might be the same word.
        replace_word = 'item{0}'.format(chr(65 +i))
        sen = sen.replace(copy_item_list[i], replace_word)
        no_spec_char_item_list.append([replace_word, copy_item_list[i]])

    label_item_transform_dict = { item[1]: [] for item in no_spec_char_item_list }

    for item in no_spec_char_item_list:
        sen_list = sen.split(item[0])
        # because of pop would do from the end
        sen_list.reverse()
        label_sen = ''
        item_label_list = []
        for i in range(0, len(sen_list)):
            label_sen += sen_list.pop()
            label = ''
            if sen_list:
                # need to check next part is different word
                # sen_list[-1] because of sen_list.reverse()
                if re.search(u'^[ \,\.\:\;\-\'\"\]\)\/~><]', sen_list[-1]) or not sen_list[-1]:
                    # checn last sentence part is different word
                    if not label_sen or re.search(u'[ \,\.\:\;\-\'\"\[\(\/~><]$', label_sen):
                        label = '{0}{1}'.format(item[0], i)
                        label_item_transform_dict[item[1]].append(label)
                else:
                    label = item[0]
                label_sen += label
            else:
                sen = label_sen
    label_set_list = []
    for item in item_list:
        label_set_list.append(label_item_transform_dict[item])
    return sen, label_set_list

if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['get_pair', 'get_tree', 'compare'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a input text')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')
    parser.add_argument('-F', '--Filter', type=str, default='filter.json', help='provide a json to filter')
    parser.add_argument('-b', '--base-file', type=str, default='INPUT2', help='provide a base file to compare polarity')

    opt = parser.parse_args(sys.argv[1:])
    if 'get_pair' == opt.option:
        text = InputText(opt.Input)
        # TODO: need method to get value if output file is not empty
        with open(opt.Output, 'w') as output_json:
            json.dump(text.data, output_json)
    elif 'get_tree' == opt.option:
        with open(opt.Input) as json_f:
            sen_list = json.load(json_f)
        results = get_parsing_tree(sen_list)
        with open(opt.Output, 'w') as output_json:
            json.dump(results, output_json)
    elif 'compare' == opt.option:
        with open(opt.Input) as json_f:
            contents = json.load(json_f)
        with open(opt.base_file) as json_bf:
            base_contents = json.load(json_bf)
        contents_count = 0
        base_polarity_dict = {}
        for base_sen in base_contents:
            # TODO not yet TODO
            #print(base_sen['polarity'])
            #contents[contents_count]
            #contents_count += 1
            for polarity in base_sen['polarity']:
                if polarity in base_polarity_dict:
                    base_polarity_dict[polarity] += 1
                else:
                    base_polarity_dict[polarity] = 1
        input_polarity_dict = {}
        for sen in contents:
            if sen['polarity'] in input_polarity_dict:
                input_polarity_dict[sen['polarity']] += 1
            else:
                input_polarity_dict[sen['polarity']] = 1
        print('Input file polarity: {0}'.format(input_polarity_dict))
        print('Base file polarity: {0}'.format(base_polarity_dict))
