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
                    if pair_info not in check_repeat_sentences_list:
                        check_repeat_sentences_list.append(dict(pair_info))
                        pair_info['polarity'] = [polarity]
                        sentences_list.append(dict(pair_info))
                    else:
                        sentences_list[
                                check_repeat_sentences_list.index(
                                    pair_info)]['polarity'].append(polarity)
        return sentences_list

def get_parsing_tree(sentences_list = []):
    import re
    import stanford_corenlp_tool as stanford_tool

    sentences_list_with_tree = []
    error_data_list = []
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
            item_list[0].reverse()
            for _ in range(0, len(item_list[0])):
                if 1 < len(item_list[0]):
                    item_pair_list.append([item_list[0].pop(), list(item_list[0])])
        else: 
            sentence_with_item_label, item_list = _label_orig_sentence_by_items(
                    sen_info['orig_sen'], [item1,item2])
            for _ in item_list[0]:
                item_pair_list.append([ _, item_list[1]])

        try:
            orig_tree = list(stanford_tool.get_parse(
                    [sentence_with_item_label])[0])
        except UnicodeDecodeError:
            continue

        check_data_correct = 0
        pair_number_in_sen = 0

        polarity_list = list(sen_info['polarity'])
        for item_pair in item_pair_list:
            re_item1 = item_pair[0]
            for re_item2 in item_pair[1]:
                # item1, 2 have to be in right order in sentence
                if not re.search('{0}.*{1}'.format(re_item1, re_item2),
                        sentence_with_item_label)\
                        or len(polarity_list) < (pair_number_in_sen + 1):
                    continue

                break_switch = 0
                for h in range(0, orig_tree[0].height()):
                    for s_tree in orig_tree[0].subtrees(lambda i: i.height() == h):
                        # unified string format for keywords and tree
                        subtree_str = _leaves_list_to_sentence(list(s_tree.leaves()))
                        item1_in_tree_number = subtree_str.count(re_item1)
                        item2_in_tree_number = subtree_str.count(re_item2)
                        # first subtree have every items
                        if item1_in_tree_number >= 1\
                                and item2_in_tree_number >= 1:
                            sen_info['pos_tree'] = s_tree.pos()
                            sen_info['pos_tree_height'] = h
                            sen_info['tree_sentence'] = s_tree.leaves()
                            sen_info['orig_sen'] = sentence_with_item_label
                            sen_info['re_drug1'] = re_item1
                            sen_info['re_drug2'] = re_item2
                            sen_info['polarity'] = polarity_list[pair_number_in_sen]
                            print(sen_info)
                            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            sentences_list_with_tree.append(sen_info)
                            pair_number_in_sen += 1
                            check_data_correct = 1
                            break_switch = 1
                            break
                    if break_switch == 1:
                        break_switch = 0
                        break
        if not check_data_correct:
            print(sen_info['orig_sen'])
            print('item1: {0}'.format(item1))
            print('item2: {0}'.format(item2))
            print('Polarity: {0}'.format(sen_info['polarity']))
            print('Item pair list: {0}'.format(item_pair_list))
            print('sentence with label: {0}'.format(sentence_with_item_label))
            print(re_item1)
            print(re_item2)
            print('-----------------------------------------------------')
            error_data_list.append(sen_info)
    print('______________________________________________________')
    print('______________________________________________________')
    print('______________________________________________________')
    import time
    with open('error_data.json' + str(time.clock()), 'w') as error_json:
        json.dump(error_data_list, error_json)
    print(error_data_list)
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
    special_char = '[^a-zA-Z0-9]'
    # need a mapping dict, because item transform need to do in order by item string's lenght
    # but label set list need to in order by item_list
    no_spec_char_item_list = []
    copy_item_list = list(item_list)
    copy_item_list.sort(key = len)
    copy_item_list.reverse()
    replace_item_list = ['itemA', 'itemB', 'itemC']
    for i in range(0, len(copy_item_list)):
        # use tag N to replace specoal word, if just remove, item1 and item2 might be the same word.
#        no_spec_char_item = re.sub(special_char, 'N', item)
#        sen = sen.replace(item, no_spec_char_item)
        sen = sen.replace(copy_item_list[i], replace_item_list[i])
        no_spec_char_item_list.append([replace_item_list[i], copy_item_list[i]])
    print(no_spec_char_item_list)

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
    print(sen)
    print(label_set_list)
    return sen, label_set_list

if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['get_pair', 'get_tree'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a input text')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')
    parser.add_argument('-F', '--Filter', type=str, default='filter.json', help='provide a json to filter')
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
