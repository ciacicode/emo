import requests
import csv
import pdb
import time
from config import Config
import numpy

##Script to collect data using sightcorp api

def get_data(image_file):
    time.sleep(1)
    json_resp = requests.post('http://api.sightcorp.com/api/detect/',
                              data={'app_key': Config.KEY,
                                    'client_id': Config.CLIENT},
                              files={'img': ('team', open(image_file, 'rb'))})

    return json_resp.json()


def collect_data(input_file, output_file):
    try:
        with open(output_file, 'w') as ofile:
            fieldnames = ['team', 'match', 'result', 'mood', 'mood_confidence', 'fear', 'anger', 'disgust', 'happiness',
                          'neutral', 'sadness', 'surprise']
            writer = csv.DictWriter(ofile, fieldnames=fieldnames)
            # write file header as a start
            writer.writeheader()
            try:
                with open(input_file, 'rb') as ifile:
                    reader = csv.DictReader(ifile)
                    for row in reader:
                        # get data for the team
                        person_details = dict()
                        d = get_data(row['file_path'])
                        for person in d['persons']:
                            # compose dict
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
            except IOError as ioe:
                print
                ioe
    except IOError as ioe:
        print
        ioe


def calculate_average():
    with open(output_file, 'rb') as ofile:
        reader = csv.DictReader(ofile)
        # create a table to contain all the data. format [[team, match, result, fear...surprise],[...]]
        result_dict= dict()
        fear_dict = dict()
        anger_dict = dict()
        disgust_dict = dict()
        happiness_dict = dict()
        neutral_dict = dict()
        sadness_dict = dict()
        surprise_dict = dict()
        counter_dict = dict()

        # for each key (team + game): sums the indexes
        for row in reader:
            key = get_data(row['team']) + '_in_' + get_data(row['match'])
            result_dict[key] = get_data(row['result'])
            fear_dict[key] = fear_dict[key] + int(row['fear'])
            anger_dict[key] = anger_dict[key] + int(row['anger'])
            disgust_dict[key] = disgust_dict[key] + int(row['disgust'])
            happiness_dict[key] = happiness_dict[key] + int(row['happiness'])
            neutral_dict[key] = neutral_dict[key] + int(row['neutral'])
            sadness_dict[key] = sadness_dict[key] + int(row['sadness'])
            surprise_dict[key] = surprise_dict[key] + int(row['surprise'])
            counter_dict[key] = counter_dict[key] + 1

    # now calculate the average
    for key in fear_dict:
        fear_dict[key] = fear_dict[key] / counter_dict[key]
        anger_dict[key] = anger_dict[key] / counter_dict[key]
        disgust_dict[key] = disgust_dict[key] / counter_dict[key]
        happiness_dict[key] = happiness_dict[key] / counter_dict[key]
        neutral_dict[key] = neutral_dict[key] / counter_dict[key]
        sadness_dict[key] = sadness_dict[key] / counter_dict[key]
        surprise_dict[key] = surprise_dict[key] / counter_dict[key]

    return fear_dict

def test():
    collect_data('/home/maria/Desktop/ciacicode/emo/data/input.csv',
                 '/home/maria/Desktop/ciacicode/emo/data/output.csv')
    fear_dict = calculate_average()
    print(fear_dict)

test()
