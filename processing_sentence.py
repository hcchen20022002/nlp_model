#!/usr/bin/python3
# coding=UTF-8

import sys, argparse

class InputText(object):
    def __init__(self, input_file):
        self.sections = self.get_section(input_file)
        self.sentences = self.get_sentence(self.sections)

    def get_section(self, file_name):
        with open(file_name, 'r') as f:
            sections_list = []
            section_value = ''
            section_line_count = 0 
            for line in f:
                if '\n' == line:
                #if ' \n' == line:
                    if 5 < section_line_count:
                        sections_list.append(section_value.replace('\n', ' ').replace('  ', ' '))
                    section_value = ''
                    section_line_count = 0

                section_line_count = section_line_count + 1
                section_value = section_value + line
        return sections_list

    def get_sentence(self, sections):
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

    #if output_file:
    #    with open(output_file, 'w') as output_f:
    #        for line in result_sentences:
    #            for _ in line:
    #                output_f.write(str(_))
    #return result_sentences
if '__main__' == __name__ :
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('-I', '--Input', type=str, default='INPUT', help='provide a ')
    parser.add_argument('-O', '--Output', type=str, default='cut_line_output.txt', help='provide a ')
    opt = parser.parse_args(sys.argv[1:])

    input_text = InputText(opt.Input)
    for _ in input_text.sentences:
        if "Parkinson's disease" in _ :
            print(_)
    #cut_line(sentences_list, opt.Output))
