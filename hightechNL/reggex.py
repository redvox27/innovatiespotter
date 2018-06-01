import re

def reggex(string):
    match = re.search(r'[A-Z]{1}[a-z]+\s\d+', string)
    if match :
        print(match.group())
    else:
        print('no result found')

reggex("Kampakkers 52")
reggex("5503 LL Veldhoven")