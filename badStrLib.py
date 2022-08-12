
def keep(str, keep):
    out = ""
    for character in str:
        if character in keep:
            out += character
    return out