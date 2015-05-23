import re


def innerStrip(strInput):
    replaceRegex = re.compile(r'\s+', re.M | re.I)
    return re.sub(replaceRegex , ' ', strInput).strip()