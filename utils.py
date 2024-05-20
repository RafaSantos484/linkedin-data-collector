import re


def extract_linkedin_id(url):
    pattern = r'(https?://)?(www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        result = match.group(3)
        if type(result) == str:
            return result
        else:
            return None
    else:
        return None
