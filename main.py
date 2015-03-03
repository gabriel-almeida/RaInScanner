__author__ = 'Gabriel'
from concurrent.futures import ThreadPoolExecutor
import itertools
import IpGenerator
import Requester
import pickle

IP_BLOCK_SIZE = 5000
dumpName = 'dump.pickle'
outputName = 'result.txt'

executor = ThreadPoolExecutor(max_workers=300)
try:
    ips, requester = pickle.load(open(dumpName, 'rb'))
    print('Pickle file were loaded')
except:
    print('Pickle file not found.')
    ips = IpGenerator.IpGenerator()
    requester = Requester.WebRequester()

output = open(outputName, 'a')
while True:
    for response in executor.map(requester.request, itertools.islice(ips.generator(), IP_BLOCK_SIZE)):
        try:
            if response is not None:
                print(response)
                output.write(str(response))
                output.write('\n')
                output.flush()
                pickle.dump((ips, requester), open(dumpName, 'wb'))
        except Exception as e:
            print('ERROR: ' + str(e))
