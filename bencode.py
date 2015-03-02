class BencodeException(Exception):
    pass


def decode_bencode(bdata):
    """Return a decoded bencode string as a Python structure."""
    return decode_data(bdata)[0]


def decode_data(bdata):
    """Return a tuple: The decoded data and
       the remainder of the encoded string."""
    if bdata[0] == 'i':
        return decode_integer(bdata[1:])
    elif bdata[0] == 'l':
        return decode_list(bdata[1:])
    elif bdata[0] == 'd':
        return decode_dict(bdata[1:])
    else:
        return decode_string(bdata)


def decode_dict(bdict):
    """Decode bencode dictionary."""
    decoded_dict = {}
    while bdict and bdict[0] != 'e':
        bkey, bdict = decode_data(bdict)
        bvalue, bdict = decode_data(bdict)
        decoded_dict[bkey] = bvalue
    return decoded_dict, bdict[1:]


def decode_integer(bint):
    """Decode bencode integer."""
    bint = bint.split('e', 1)
    try:
        integer = int(bint[0])
    except ValueError:
        raise BencodeException('Bad bencode at %s' % (bint))
    return integer, bint[1]


def decode_list(blist):
    """Decode bencode list."""
    decoded_list = []
    while blist and blist[0] != 'e':
        decoded_data = decode_data(blist)
        decoded_list.append(decoded_data[0])
        blist = decoded_data[1]
    return decoded_list, blist[1:]


def decode_string(bstring):
    """Decode bencode string."""
    length, string = bstring.split(':', 1)
    length = int(length)
    bdata = string[length:]
    string = string[:length]
    if len(string) != length:
        raise BencodeException('Bad bencode at %s' % (bstring))
    return string, bdata
