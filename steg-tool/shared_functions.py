#convert a supplied string to a usable integer
def string_to_num(str : str):
    total = 0
    for index in range(len(str)): total += ord(str[index][0])
    return total

#take in a seed base and top to give a semi-random number
def get_pseudorandom(seed, base, top):
    seed, base, top = int(seed), int(base), int(top) # make sure inputs are the proper format
    
    #remove the 0b string from the beggining of the binary string
    seed_binary = bin(seed)[2:]
    top_binary = bin(top)[2:]

    #make sure both strings are the same length, and add to the begging of the shorter one
    extra_zeros = len(seed_binary) - len(top_binary)
    if extra_zeros > 0:
        for i in range(0, extra_zeros, 1): top_binary = "0" + top_binary
    if extra_zeros < 0:
        for i in range(0, extra_zeros, -1): seed_binary = "0" + seed_binary
    
    #preform and XOR (exclusive or) function on the top and seed binary
    return_num = ""
    for index in range(len(top_binary)):
        if seed_binary[index] == top_binary[index]: return_num = return_num + "0"
        else: return_num = return_num + "1"
    
    #convert the number back to integer
    num = 0
    for index, value in enumerate(return_num):
        num += int(value) * 2 ** index
    return_num = num
    del num

    return min(max(((return_num ** 3 + base) ** 2 % (top - base)) + base, base), top - 1) #further randomize the returned number