import re
def match(text):
    pattern = r'\Bz\B'
    if re.findall(pattern, text):
        return 'a match found'
    else:
        return 'not match'
print(match('The quick brown fox jumps over the lazy dog'))
print(match('zahra'))