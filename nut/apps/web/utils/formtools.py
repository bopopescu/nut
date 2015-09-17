import re

def innerStrip(strInput):
    replaceRegex = re.compile(r'\s+', re.M | re.I)
    return re.sub(replaceRegex , ' ', strInput).strip()


translateTable = dict((ord(char), None) for char in "<>\'\"&;")
strict_translateTable=dict((ord(char), None) for char in "<>\'\"&;)(:")
def clean_user_text(contents):
     if not isinstance(contents, unicode):
        contents = unicode(contents)
     return contents.translate(translateTable)

def clean_user_text_strict(contents):
    if not isinstance(contents, unicode):
        contents = unicode(contents)
    return contents.translate(strict_translateTable)

if __name__=="__main__":
    content = '<script language="javascript">alert("ant");</script>'
    print clean_user_text(content)
    print clean_user_text_strict(content)