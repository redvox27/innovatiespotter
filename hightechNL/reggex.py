import re

def reggex(string):
    match = re.search(r'\d{4}? [A-Z]{2}? [A-Z]{1}[a-z]+', string)
    if match:
        print(match.group())
    else:
        print('no result found')

reggex("5652 XR Eindhoven")
reggex("5503 LL Veldhoven")