import bleach


articleContentAllowedTags = ['p', 'em', 'strong', 'div', 'ul', 'ol', 'li','a','br','span','img']
allowedAttrs = {
    '*': ['class'],
    'a': ['href', 'rel'],
    'img': ['src', 'alt'],
}
def contentBleacher(content):
    return bleach.clean(content, tags=articleContentAllowedTags,\
                                 attributes=allowedAttrs,\
                                 strip_comments=True, strip=True)
