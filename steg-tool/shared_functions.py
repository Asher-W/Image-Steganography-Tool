# convert a supplied string to a usable integer
def string_to_num(str : str):
    return sum([ord(str[index]) for index in range(len(str))])

def xor(n1, n2):
    # remove the 0b string from the beggining of the binary string
    n1_binary, n2_binary = bin(n1)[2:], bin(n2)[2:]

    # make sure both strings are the same length, and add to the begging of the shorter one
    extra_zeros = len(n1_binary) - len(n2_binary)
    if extra_zeros > 0:
        for i in range(0, extra_zeros, 1): n2_binary = "0" + n2_binary
    if extra_zeros < 0:
        for i in range(0, extra_zeros, -1): n1_binary = "0" + n1_binary
    
    # preform and XOR (exclusive or) function on the top and seed binary
    return_num = ""
    for index in range(len(n2_binary)):
        if n1_binary[index] == n2_binary[index]: return_num = return_num + "0"
        else: return_num = return_num + "1"
    
    return_num = sum([int(value) * (2 ** index) for index, value in enumerate(return_num)])

    return return_num

# take in a seed base and top to give a semi-random number
def get_sudo_random(seed, base, top):
    seed, base, top = int(seed), int(base), int(top) # make sure inputs are the proper format
    
    return_num = xor(xor(seed, top) ** 3, base)
    
    return (((return_num ** 2 + base ** 3) + return_num)  % (top - base)) + base # further randomize the returned number