import hammer as h


digit   = h.ch_range('0','9')
upper   = h.ch_range('A', 'Z')
lower   = h.ch_range('a', 'z')
chars   = h.choice(digit, upper, lower)

alphanumeric = h.many(chars)

words = h.sepBy1(alphanumeric, h.ch(' '))
version = h.token("Version")
allchars = h.ch_range("!", "~")

printable_chars = h.many(allchars)

token = h.many1(printable_chars)
tokens = h.sepBy1(printable_chars, h.choice(h.ch(' '), h.ch('\n'), h.ch('\r')))

# Action Modifiers

def tuple_string(t):
    new_coll = list()
    for c in t:
        if isinstance(c, tuple):
                new_coll.append("".join(c))
        else:
            return "".join(t)
    return tuple(new_coll)


# FastIron Parsers




# FastIron Combinators

def get_version(text):
    version_string = h.right(h.token("SW: Version "), h.sepBy(alphanumeric, h.ch('.')))
    version = h.whitespace(version_string)
    parser = h.action(version, tuple_string)
    for i in text.split("\n"):
        ret = parser.parse(i.encode('ascii','ignore'))
        if ret is not None:
            return {'os_version': ".".join(ret)}
