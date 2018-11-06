
import json
import os
import sys

def save_file(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


print("Decoded meta.json file")

print("args count: ", len(sys.argv))

basePath = ''

if len(sys.argv) > 1:
    fileName = sys.argv[1]
    if os.path.exists(fileName):
        with open(fileName, 'r') as inputfile:
            result = json.load(inputfile)

            print("table title: ", result['tables'][7]['title'])
            save_file(fileName, result)


