class BencodeException(Exception):
    pass


def decode_bencode(bdata):
    if bdata[0] == 'i':
        split_list = bdata.split('e', 1)
        return decode_integer(split_list[0][1:]), split_list[1]
    elif bdata[0] == 'l':
        split_list = bdata.split('e', 1)
        return decode_list(bdata[1:]), split_list[1]
    elif bdata[0] == 'd':
        split_list = bdata.split('e', 1)
        # print bdata[1:]
        return decode_dict(bdata[1:]), split_list[1]

def decode_dict(bdict):
    decoded_dict = {}
    while bdict and bdict[0] != 'e':
        bkey, bdict = decode_bencode(bdict)
        bvalue, bdict = decode_bencode(bdict)
        decoded_dict[bkey] = bvalue
    return decoded_dict

def decode_integer(bint):
    try:
        integer = int(bint)
    except ValueError:
        raise BencodeException('Bad bencode at %s' % (bint))
    return integer

def decode_list(blist):
    decoded_list = []
    while blist and blist[0] != 'e':
        decoded_data = decode_bencode(blist)
        decoded_list.append(decoded_data[0])
        blist = decoded_data[1]
    return decoded_list

def decode_string(bstring):
    (length, string) = bstring.split(':')
    if len(string) != int(length):
        raise BencodeException('Bad bencode at %s' % (bstring))
    return string
