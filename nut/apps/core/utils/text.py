def truncate(value, length=50):
    if len(value) < length:
        return value
    else:
        return value[:length]

