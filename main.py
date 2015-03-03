__author__ = 'Gabriel'
from concurrent.futures import ThreadPoolExecutor
import itertools
import IpGenerator
import Requester

#TODO Refactor

IP_BLOCK_SIZE = 50000
outputName = 'result.txt'

executor = ThreadPoolExecutor(max_workers=500)
ips = IpGenerator.IpGenerator()
requester = Requester.WebRequester()

try:
    f = open(outputName, 'r')
    for line in f:
        ip = line.split(',', maxsplit=1)[0].strip("(\'http:\/\/")
        ips._used.add(ip)
    print('Last run IP were loaded')
except:
    print('Begining new scan.')

output = open(outputName, 'a')
while True:
    for response in executor.map(requester.request, itertools.islice(ips.generator(), IP_BLOCK_SIZE)):
        try:
            if response is not None:
                print(response)
                output.write(str(response))
                output.write('\n')
                output.flush()
        except Exception as e:
            print('ERROR: ' + str(e))
