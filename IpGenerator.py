__author__ = 'Gabriel'
import random


class IpGenerator():
    #TODO Accept ip mask
    #TODO increase performance
    #TODO refactor generator method

    def __init__(self):
        self._used = set()

    def generator(self):
        while True:
            oct = [random.randint(0, 255) for i in range(4)]
            if oct[0] == 10 or (oct[0] == 172 and oct[1]>=16 and oct[1] <=31) or\
                    (oct[0] == 192 and oct[1] == 16) or\
                     oct[-1] == 255 or oct[-1] == 0:
                continue
            ip = '.'.join(map(lambda s: str(s), oct))
            if ip in self._used:
                continue
            self._used.add(ip)
            yield ip

if __name__ == '__main__':
    import itertools
    ips = IpGenerator().generator()
    [ print(i) for i in itertools.islice(ips, 10)]