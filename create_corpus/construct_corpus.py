#!/usr/bin/python3
# coding=UTF-8

import sys, argparse, json

class InputText(object):
    def __init__(self, input_file):
        self.sections = self.get_section(input_file)
        self.sentences = self.get_sentence()

    def get_section(self, file_name):
        with open(file_name, 'r') as f:
            sections_list = []
            section_value = ''
            section_line_count = 0
            ignore_flag = False
            ignore_list = ['Author information:']

            for line in f:
                # last line in section
                if '\n' == line:
                #if ' \n' == line:
                    if 4 < section_line_count and not ignore_flag:
                        sections_list.append(section_value.replace('\n', ' ').replace('  ', ' '))
                    section_value = ''
                    section_line_count = 0
                    ignore_flag = False
                
                for ignore_word in ignore_list:
                    if ignore_word in line:
                        ignore_flag = True
                        break
                section_line_count = section_line_count + 1
                section_value = section_value + line
        return sections_list

    def get_sentence(self):
        sections = self.sections
        sentence_list = []
        sentence = ''
        word = ''
        for sec in sections:
            for letter in sec:
                word = word + letter
                if ' ' == letter:
                    sentence = sentence + word
                    if '.' in word and '.' == word[-2]:
                        sentence_list.append(sentence)
                        sentence = ''
                    word = ''
        return sentence_list

def filter_keys_to_json(sentences_list = [], filter_json = ""):
    match_sentences_list = []
    with open(filter_json) as filterF:
        json_file = json.load(filterF)
        filter_keys = json_file['data']
    for key in filter_keys:
        for sen in sentences_list:
            if key.lower() in sen.lower():
                for depands_key in filter_keys[key]:
                    if depands_key[0].lower() in sen.lower():
                        match_sentences_list.append({
                            "orig_sen" : sen,
                            "drug" : key,
                            "disease": depands_key[0],
                            "polarity": depands_key[1]
                            })
    return match_sentences_list

def get_parsing_tree(sentences_list = []):
    import re
    import stanford_corenlp_tool as stanford_tool

    sentences_list_with_tree = []
    for _ in range(0, len(sentences_list)):
        sen_info = sentences_list.pop()
        if 1 == sen_info['polarity']:
            continue
        print(sen_info['orig_sen'])
        print('Drug: {0}'.format(sen_info['drug']))
        print('Disease: {0}'.format(sen_info['disease']))
        print('Polarity: {0}'.format(sen_info['polarity']))
        # [0][0] at the end is because get_parse() would return a list
        # this list only have 1 element by which we input only 1 too
        
        if re.findall(u'[\u4e00-\u9fff]+', sen_info['orig_sen']):
            print('Have chinese!')
            continue
        try:
            orig_tree = stanford_tool.get_parse(
                [sen_info['orig_sen']])[0]
        except UnicodeDecodeError:
            continue

        break_switch = 0
        for i in orig_tree:
            for h in range(0, i.height()):
                for s_tree in i.subtrees(lambda i: i.height() == h):
                    # unified string format for keywords and tree
                    drug = _unified_string(sen_info['drug'])
                    disease = _unified_string(sen_info['disease'])
                    tree_leaves = [ _.lower() for _ in s_tree.leaves()]
                    #if set(drug).issubset(tree_leaves)\
                            #and set(disease).issubset(tree_leaves):
                    if any( _d in _l for _d in drug for _l in tree_leaves)\
                            and any( _di in _l for _di in disease for _l in tree_leaves):
                        sen_info['pos_tree'] = s_tree.pos()
                        sen_info['pos_tree_height'] = h
                        sen_info['tree_sentence'] = s_tree.leaves()
                        sentences_list_with_tree.append(sen_info)
                        print('Subtree height: {0}'.format(h))
                        print(s_tree.pos())
                        print(s_tree.leaves())
                        break_switch = 1
                        break
                if break_switch == 1:
                    break_switch = 0
                    break
            print('__________________________________________')
        print('=======================================')
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


if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['split', 'filter', 'get_tree'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a input text')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')
    parser.add_argument('-F', '--Filter', type=str, default='filter.json', help='provide a json to filter')
    opt = parser.parse_args(sys.argv[1:])



    if 'split' == opt.option:
        text = InputText(opt.Input)
        with open(opt.Output, 'w') as output_f:
            for sen in text.sentences:
                for _ in sen:
                    output_f.write(str(_))
                output_f.write('\n')
    elif 'filter' == opt.option:
        text = InputText(opt.Input)
        # it's for two items relationships
        filter_result = filter_keys_to_json(text.sentences, opt.Filter)
        with open(opt.Output, 'w') as output_json:
            json.dump(filter_result, output_json)
        #for _ in filter_result:
        #    print(_['disease'])
    elif 'get_tree' == opt.option:
        with open(opt.Input) as json_f:
            sen_list = json.load(json_f)
        results = get_parsing_tree(sen_list)
        with open(opt.Output, 'w') as output_json:
            json.dump(results, output_json)

