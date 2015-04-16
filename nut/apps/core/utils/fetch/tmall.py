#encoding=utf8

import requests


def test():
    r = requests.get('http://www.sina.com');
    print dir(r);
    pass

if __name__ == "__main__":
    test();