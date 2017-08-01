#!/usr/bin/python -B

import sys, os
import argparse, time, json

def func_timer(fn):
    def with_timer(*args, **kwargs):
        start = time.time()

        fn_return_value = fn(*args, **kwargs)

        end = time.time()
        elapsed = end - start
        print "Time taken: ", elapsed, "seconds."
        return fn_return_value
    return with_timer

def check_file_exists(file_name):
    if not os.path.isfile(file_name):
        print("There are no file : {0}".format(file_name))
        exit()
    return True

@func_timer
def search_match_section(input_file, output_file, keyword):
    import re
    match_sections = []
    section = []
    match_flag = 0
    section_flag = 0
    with open(input_file, 'r') as f:
        for line in f :
            if re.search('Study [0-9]+:', line):
                section_flag = 1
            if len(line) == 2:
                section_flag = 0
            #
            if keyword in line:
                match_flag = 1
                section.append(line)
            if 'Conditions' in line:
                section.append(line)
            #
            #section.append(line)
            #if keyword in line:
            #    match_flag = 1
            #
            if section_flag == 0:
                if match_flag == 1:
                    match_sections.append(section)
                    match_flag = 0
                section = []

    with open(output_file, 'w') as output_f:
        line_with_key = ''
        for sec in match_sections:
            for l in sec:
                #output_f.write(l)
                line_with_key = line_with_key + l
            output_f.write(line_with_key + '\n\n')
            line_with_key = ''

if __name__ == '__main__':
    #search_match_section('study_fields.txt', 'study_fields_PD.txt', "Parkinson's Disease")
    search_match_section('study_fields_PD.txt', 'study_fields_drug&PD.txt', 'Drug')
