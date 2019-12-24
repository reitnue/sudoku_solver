import sys
import json

if __name__ == '__main__':
    # test1
    with open('../test/test1.json', 'r') as test1_file:
        test1 = json.loads(test1_file.read())

    for x in test1:
        print(' '.join(map(str, x)))