def paginate(cursor, page, per_page):
    skip = (page - 1) * per_page
    return cursor.skip(skip).limit(per_page)
