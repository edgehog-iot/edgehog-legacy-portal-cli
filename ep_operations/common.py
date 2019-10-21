HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def get_authorized_headers(token:str):
    authorized_headers = HEADERS.copy()
    authorized_headers['Authorization'] = 'Bearer {}'.format(token)
    return authorized_headers
