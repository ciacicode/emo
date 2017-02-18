import requests
import csv
import pdb
import time
from config import Config
import os

##Script to collect data using sightcorp api

def get_data(image_file):
    time.sleep(1)
    working_directory = os.getcwd()
    json_resp = requests.post( 'http://api.sightcorp.com/api/detect/',
              data   = { 'app_key'   : Config.KEY,
                         'client_id' : Config.CLIENT},
              files  = { 'img'       : ( 'team', open( working_directory + image_file, 'rb' ) ) } )

    return json_resp.json()

def collect_data(input_file, output_file):
    try:
        with open(output_file,'wa') as ofile:
            fieldnames = ['team', 'match', 'result', 'mood', 'mood_confidence','fear','anger','disgust','happiness','neutral','sadness','surprise']
            writer = csv.DictWriter(ofile, fieldnames=fieldnames)
            #write file header as a start
            writer.writeheader()
            try:
                with open(input_file, 'rb') as ifile:
                    reader = csv.DictReader(ifile)
                    for row in reader:
                        #get data for the team
                        person_details = dict()
                        d = get_data(row['file_path'])
                        for person in d['persons']:
                            #compose dict
                            try:
                                person_details['team'] = row['team']
                                person_details['match'] = row['match']
                                person_details['result'] = row['result']
                                person_details['mood'] = person['mood']['value']
                                person_details['mood_confidence'] = person['mood']['confidence']
                                person_details['anger'] = person['expressions']['anger']['value']
                                person_details['disgust'] = person['expressions']['disgust']['value']
                                person_details['fear'] = person['expressions']['fear']['value']
                                person_details['happiness'] = person['expressions']['happiness']['value']
                                person_details['neutral'] = person['expressions']['neutral']['value']
                                person_details['sadness'] = person['expressions']['sadness']['value']
                                person_details['surprise'] = person['expressions']['surprise']['value']
                                writer.writerow(person_details)
                            except KeyError as ke:
                                print ke
                                print person
            except IOError as ioe:
                print ioe
    except IOError as ioe:
        print ioe
    
def test():
    working_directory = os.getcwd()
    collect_data(working_directory + '/data/input.csv',working_directory + '/data/output.csv')