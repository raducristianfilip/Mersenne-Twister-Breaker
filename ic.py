from datetime import datetime
import time

# Create a length n array to store the state of the generator, n = 64
MT = [0 for i in range(624)]
index = 624


#(w, n, m, r) = (32, 624, 397, 31)

# To get last 32 bits
get_last_32_bits = (1 << 32) - 1

# To get last 31 bits
lower_mask = (1 << 31) - 1

# To get 32. bit
upper_mask = (~lower_mask) & get_last_32_bits

f = 1812433253
w = 32
d = 4294967295


# Initialize the generator from a seed
def initialize_generator(seed):
    "Initialize the generator from a seed"
    global MT
    global get_last_32_bits
    global f
    global w
    MT[0] = seed
    for i in range(1, 624):
        MT[i] = (f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i) & get_last_32_bits

def extract_number():
    global index
    global MT
    global d
    if index >= 624:
        if index > 624:
            print "EROARE"
        else:
            twist()

    #tempering
    y = MT[index]

    y ^= (y >> 11)  # u = 11
    y ^= ((y << 7) & 2636928640)  # b in baza 16
    y ^= ((y << 15) & 4022730752)  # c in baza 16
    y ^= y >> 18  # l

    index = (index + 1)
    return y

def twist():
    # Generate the next n values from the series x_i
    global MT
    global index
    for i in range(624):
        x = (MT[i] & upper_mask) + (MT[(i + 1) % 624] & lower_mask)
        xA = x >> 1
        if x % 2 != 0:
            xA = xA ^ 2567483615 #a in baza 16
        MT[i] = MT[(i+397) % 624] ^ xA
    index = 0


def decimalToBinary(n):
    return bin(n).replace("0b","")

def unshiftRightXor(x, shift):
    res = x
    count = 0
    aux = 0
    while True:
        if aux ^ res == 0 and count >= 1:
            break
        aux = res
        res = res >> shift
        res = x ^ res
        count += 1
    return res

def unshiftLeftXor(x, shift, mask):
    res = x
    count = 0
    aux = 0
    while True:
        if aux ^ res == 0 and count >= 1:
            break
        aux = res
        res = res << shift & mask
        res = x ^ res
        count += 1
    return res

def predict(values):
    for i in range(624):
        x = (values[i] & upper_mask) + (values[(i + 1) % 624] & lower_mask)
        xA = x >> 1
        if x % 2 != 0:
            xA = xA ^ 2567483615  # a in baza 16
        values[i] = values[(i + 397) % 624] ^ xA
    return values

#untemper function to determine the internal value of a generated number
def untemper(v):
    #unshifting functions to determine numberes before tempering.
    v = unshiftRightXor(v, 18)
    v = unshiftLeftXor(v, 15, 4022730752)
    v = unshiftLeftXor(v, 7, 2636928640)
    v = unshiftRightXor(v, 11)
    return v

if __name__ == "__main__":
    seed = 5489
    start = time.time()
    rnd_seed = datetime.now()
    initialize_generator(rnd_seed.microsecond)

    outputs = []
    #initialize_generator(seed)

    for i in range(624):
        outputs.append(extract_number())

    print "MT:"
    print MT

    print "624 generated values:"
    print outputs

    internal_state = []

    for i in range(len(outputs)):
        internal_state.append(untemper(outputs[i]))

    print "Untempered Values => Internal States:"
    print internal_state

    next_states = predict(internal_state)
    outputs = []
    print index

    for i in range(624):
        outputs.append(extract_number())

    print "Predicted values:"
    print next_states

    print "New MT after 624 were generated:"
    print MT


    ok = 1
    for i in range(len(next_states)):
        if next_states[i] != MT[i]:
            ok = 0

    if ok == 1:
        print "Result: Predicted"
    else:
        print "Result: Failed"

    print(time.time() - start)