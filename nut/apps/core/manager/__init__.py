def dictfetchall(cursor):

    desc = cursor.description

    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


__author__ = 'edison7500'
