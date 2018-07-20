check_list = ['/contact', 'www']
href = 'http://www.eco-logisch.com/over-ons/contact'


def is_complete_url(href):
    check_list = ['/contact', 'www']
    count = 0

    for element in check_list:
        if element in href:
            count += 1

    if count == 2:
        return True
    else:
        return False

is_complete_url(href)