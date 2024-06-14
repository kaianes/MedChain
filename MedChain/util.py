def strg2hex(string):
    return "0x" + string.encode ('utf-8').hex()

def hex2strg(hex):
    return bytes.fromhex(hex[2:])

