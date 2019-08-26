import random
import string


def make_safe_title(s):
    from string import ascii_lowercase
    return ''.join(x if x in ascii_lowercase + '_-0123456789' else
                   '-' if x == ' ' else '' for x in s.lower())


def generate_random_string(size=8, charset=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(charset) for _ in range(size))
