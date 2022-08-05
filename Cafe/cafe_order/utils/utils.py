import re
from django import template

def  create_user_name(email):
    match = re.match('(.+)@.*',email)
    # print(match.group(1))
    return match.group(1)


