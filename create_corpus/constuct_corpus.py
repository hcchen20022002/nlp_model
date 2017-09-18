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


if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('option', choices=['split', 'filter'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a input text')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a file to save output')
    parser.add_argument('-F', '--Filter', type=str, default='filter.json', help='provide a json to filter')
    opt = parser.parse_args(sys.argv[1:])

    text = InputText(opt.Input)

    if 'split' == opt.option:
        with open(opt.Output, 'w') as output_f:
            for sen in text.sentences:
                for _ in sen:
                    output_f.write(str(_))
                output_f.write('\n')
    if 'filter' == opt.option:
        # it's for two items relationships
        filter_result = filter_keys_to_json(text.sentences, opt.Filter)
        with open(opt.Output, 'w') as output_json:
            json.dump(filter_result, output_json)
        #for _ in filter_result:
        #    print(_['disease'])

