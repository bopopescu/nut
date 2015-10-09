import re

def get_entity_list_from_article_content(content):
    regstr = r"data_entity_hash=\"(\w+)\""
    regObj = re.compile(regstr, re.MULTILINE)
    result = regObj.findall(content)
    return result

if __name__ == '__main__':
    content = '<div guoku_ele="True" class="guoku-card container-fluid" data_entity_hash="9041c999"><div guoku_ele="True" class="guoku-card container-fluid" data_entity_hash="90423c999">'
    print(get_entity_list_from_article_content(content))

