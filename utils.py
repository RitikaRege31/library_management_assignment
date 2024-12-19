import secrets

def generate_token():
    return secrets.token_hex(16)

def paginate(query, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return query[start:end]
