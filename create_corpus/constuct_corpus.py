#!/usr/bin/python3
# coding=UTF-8

import sys, argparse

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

    def filter_keywords(self, keywords_list = []):
        for word in keywords_list:
            return list(filter(lambda x: word in x, self.sentences))

if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    #parser.add_argument('option', choices=['tagger', 'parser'], help='provide a action you want to do')
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a ')
    parser.add_argument('-O', '--Output', type=str, default='OUTPUT', help='provide a ')
    opt = parser.parse_args(sys.argv[1:])

    text = InputText(opt.Input)
    sentences_list = text.filter_keywords(["Parkinson's disease"])
    with open(opt.Output, 'w') as output_f:
        for sen in sentences_list:
            for _ in sen:
                output_f.write(str(_))
            output_f.write('\n')
