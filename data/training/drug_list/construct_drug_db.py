#!/usr/bin/python3 -B

import sys, os
import argparse, time, json

def check_file_exists(file_name):
    if not os.path.isfile(file_name):
        print("There are no file : {0}".format(file_name))
        exit()
    return True

def search_match_section(input_file, output_file):
    import re
    drug_list = []
    with open(input_file, 'r') as f:
        for line in f :
            for drug in line.split(', '):
                drug = drug.replace('\r\n', '')
                if drug not in drug_list:
                    drug_list.append(drug)
    for drug in drug_list:
        print(drug)

'''
    with open(output_file, 'w') as output_f:
        line_with_key = ''
        for sec in match_sections:
            for l in sec:
                #output_f.write(l)
                line_with_key = line_with_key + l
            output_f.write(line_with_key + '\n\n')
            line_with_key = ''
'''
if __name__ == '__main__':
    #search_match_section('study_fields.txt', 'study_fields_PD.txt', "Parkinson's Disease")
    search_match_section('HC_drug.txt', 'drug.json')
