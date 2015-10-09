import re

def get_entity_list_from_article_content(content):
    regstr = r"data_entity_hash=(\w+)"
    regObj = re.compile(regstr, re.MULTILINE)
    result = regObj.match(content)
    return result.groups()

if __name__ == '__main__':
    content = 'content'