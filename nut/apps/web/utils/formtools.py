import re


def innerStrip(str_input):
    replace_regex = re.compile(r'\s+', re.M | re.I)
    return re.sub(replace_regex, ' ', str_input).strip()


translate_table = {ord(char): None for char in "<>\'\"&;"}
strict_translate_table = {ord(char): None for char in "<>\'\"&;)(:"}


def clean_user_text(contents):
    if not isinstance(contents, unicode):
        contents = unicode(contents)
    return contents.translate(translate_table)


def clean_user_text_strict(contents):
    if not isinstance(contents, unicode):
        contents = unicode(contents)
    return contents.translate(strict_translate_table)


if __name__ == "__main__":
    content = '<script language="javascript">alert("ant");</script>'
    print clean_user_text(content)
    print clean_user_text_strict(content)
