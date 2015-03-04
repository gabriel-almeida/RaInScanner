__author__ = 'Gabriel'
import re
import collections
PARSER_REGEXP = re.compile('''\('(?P<ip>.*)', '(?P<title>.*)', '(?P<md5>.*)', '(?P<sha1>.*)', '(?P<page>.*)', '(?P<date>.*)'\)''')

outputName = 'result.txt'
signatureName = 'knownSignatures.csv'


def sign(info_dict):
    """ Utility function that gets a dict-like object and
    return a tuple of the fields md5 and sha1. Used in class Signature """
    return info_dict['md5'], info_dict['sha1']


class Signature():
    def __init__(self, signature_file_name=signatureName):
        self._sign_regexp = re.compile('''"(?P<md5>.*)";"(?P<sha1>.*)";"(?P<category>.*)";"(?P<description>.*)"''')
        self._signatures = dict()
        for line in open(signature_file_name, 'r'):
            match = self._sign_regexp.match(line)
            if match is not None:
                info_dict = match.groupdict()
                signature = sign(info_dict)
                current_category = info_dict['category']
                current_description = info_dict['description']
                self._signatures[signature] = (current_category, current_description)

    def category(self, info_dict):
        s = sign(info_dict)
        if s in self._signatures:
            return self._signatures[s][0]

    def description(self, info_dict):
        s = sign(info_dict)
        if s in self._signatures:
            return self._signatures[s][1]

    def categorize(self, iterable):
        categorization = dict()
        for i in iterable:
            current_category = self.category(i)
            current_description = self.description(i)
            if current_category not in categorization:
                categorization[current_category] = dict()
            if current_description not in categorization[current_category]:
                categorization[current_category][current_description] = 0
            categorization[current_category][current_description] += 1
        return categorization

if __name__ == "__main__":
    f = open(outputName, 'r')
    data = list()
    for line in f:
        match = PARSER_REGEXP.match(line)
        if match is not None:
            info_dict = match.groupdict()
            data += [info_dict]

    s = Signature()

    import pprint
    pprint.pprint(s.categorize(data))

    signatures = list(map(sign, data))
    counter = collections.Counter(signatures)
    print("\nTop 30 most common signatures not known:")
    for i in counter.most_common(30):
        signature = i[0]
        if signature in s._signatures:
            continue

        examples = list()
        lastIndex = -1
        for repetition in range(3):
            index = signatures.index(signature, lastIndex + 1)
            examples.append(data[index]['ip'])
            lastIndex = index

        print('"' + '";"'.join(signature) + '"', 'Example Ip:', examples, 'Occurrences:', i[1],  'title:', data[lastIndex]['title'])
