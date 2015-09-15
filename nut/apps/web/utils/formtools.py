import re

def innerStrip(strInput):
    replaceRegex = re.compile(r'\s+', re.M | re.I)
    return re.sub(replaceRegex , ' ', strInput).strip()


translateTable = dict((ord(char), None) for char in "<>()\'\"&")
def clean_user_text(contents):
     if not isinstance(contents, unicode):
        contents = unicode(contents)
     return contents.translate(translateTable)
