#Diffie-Hellamn - man in the middle simulation
import math
import numpy as np
import random
import copy

def generate_prime_number(range_max): #standard prime number generating algorithm
    iterator =0
    k = d = 1 #helper variables for generating 6k+1
    p = 2 # first prime
    primes = [2,3,5]
    while(iterator < range_max):
        p = 6*k + d
        if (d==1):
            d = -1
            k += 1
        else :
            d =1
        boundry = math.sqrt(p)
        i = 2
        while(primes[i]<=boundry):
            if p%primes[i] ==0:
                break
            i+=1
        primes.append(p)
        iterator+=1
    half = int(len(primes)/2)
    primes= primes[half:] # so the number is bigger
    out=random.choices(primes, k=1) 
    return out

#public - variables known to everyone
g = random.choices([2,5], k=1)[0] # choose g, usually 2 or 5
p = generate_prime_number(100)[0] # generate prime number

#private 
# known only to alice
a = random.randint(1 , p-1) #alice generates random a
A = (g**a)%p #alice performs an operation with her random number
# known only to bob
b = random.randint(1, p-1) #bob generates random b
B = (g**b)%p #bob performs an operation with his random number

#SAFE CONNECTION
#bob sends B to alice  & alice sends A to bob 
#they repeat their operation on receieved values and in the result they get matching keys - 
Ka = (B**a)%p
Kb = (A**b)%p
#Ka = Kb = k

#MAN IN THE MIDDLE model

#Eve generates random c and performs her operation on it
c = random.randint(1, p-1)
E = (g**c)%p
#Eve breaks the connection and redirects Alice computer signal to her own computer 
#Eve sets up connection with bob and acts as if she was alice
#Eve receives A form Alice and B from Bob and performs her operation on them
#Eve sends both Alice and Bob her E - Alice and Bob do not know about Eve

#Alice performs her operation on E
#Alice - Eve 
kA = (E**a)%p
kAE = (A**c)%p
print("Alice - Eve key " + str(kA))
#Bob does the same
#Bob - Eve
kB= (E**b)%p
kAE = (B**c)%p
print("Bob - Eve key " + str(kB))
#thanks to that Eve has set of 2 keys - one to connect with alice and another to connect with bob
#Alice and bob have no idea there is someone between them

#PROGRAM

#read file&convert to binary and split to 8 bit blocks -message
file = open('plaintext.txt')
data = file.read()
helper_str = ""
message_binary = []
for c in data:
    helper_str += format(ord(c), 'b')
    if (len(helper_str) < 8):
        helper_str = helper_str.rjust(8,"0")
    message_binary.append(helper_str)
    helper_str=""
file.close()

#convert all keys to binary 8 bit blocks
key_AE = format(kA, 'b')
key_BE = format(kB, 'b')
if(len(key_AE)<8):
    key_AE = key_AE.rjust(8, "0")
if(len(key_BE)<8):
    key_BE = key_BE.rjust(8, "0")
    
vec = np.random.randint(2, size = 8) #init vector
    
#------ECB------
#alice is conding
ECB_encoded =[]
for block in message_binary:
    for i in range(8):
        helper_str += str(int(block[i])^int(key_AE[i]))
    ECB_encoded.append(helper_str)
    helper_str =""
    
#eve is decoding
ECB_decoded =[]
for block in ECB_encoded:
    for i in range(8):
        helper_str += str(int(block[i])^int(key_AE[i]))
    ECB_decoded.append(helper_str)
    helper_str = ""
    
#eve is coding using Bob-Eve key
ECB_encoded_to_bob =[]
for block in ECB_decoded:
    for i in range(8):
        helper_str += str(int(block[i])^int(key_BE[i]))
    ECB_encoded_to_bob.append(helper_str)
    helper_str = ""
    
#Bob is decoding
ECB_decoded_bob =[]
for block in ECB_encoded_to_bob:
    for i in range(8):
        helper_str += str(int(block[i])^int(key_BE[i]))
    ECB_decoded_bob.append(helper_str)
    helper_str = ""
    
#Bob decoding to text
ECB = ""
for block in ECB_decoded_bob:
    ECB += chr(int(block, 2))
print("in the end bob recieved '" + ECB + "' using ECB")


#--------CBC-----------
#alice is coding the message
bit_CBC = copy.deepcopy(message_binary)
block1 = bit_CBC[0]
for i in range(8):
    helper_str+= str(int(block1[i])^vec[i]^int(key_AE[i])) #XOR first block
bit_CBC[0] = helper_str
CBC_encoded =[]
CBC_encoded.append(helper_str)
helper_str = ""
j = 0
for block in bit_CBC:
    if j>0:
        cipher_block = CBC_encoded[j-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_AE[i]))
        CBC_encoded.append(helper_str)
        helper_str = ""
    j+=1
    
# eve is decoding using Alice-Eve key
block1_eve_CBC = CBC_encoded[0]
for i in range(8):
    helper_str += str(int(block1_eve_CBC[i])^vec[i]^int(key_AE[i]))
CBC_decoded_eve =[]
CBC_decoded_eve.append(helper_str)
helper_str = ""
g = 0
for block in CBC_encoded:
    if g>0:
        cipher_block =  CBC_encoded[g-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_AE[i]))
        CBC_decoded_eve.append(helper_str)
        helper_str =""
    g+=1
    
# eve is coding using Bob_Eve key and sends the message to bob
block1_eve_bob = CBC_decoded_eve[0]
for i in range(8):
    helper_str+= str(int(block1_eve_bob[i])^vec[i]^int(key_BE[i])) #XOR first block
CBC_decoded_eve[0] = helper_str
CBC_encoded_to_bob =[]
CBC_encoded_to_bob.append(helper_str)
helper_str = ""
j = 0
for block in CBC_decoded_eve:
    if j>0:
        cipher_block = CBC_encoded_to_bob[j-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_BE[i]))
        CBC_encoded_to_bob.append(helper_str)
        helper_str = ""
    j+=1
    
#bob is decoding recieved message using bob-eve key
block1_bob = CBC_encoded_to_bob[0]
for i in range(8):
    helper_str += str(int(block1_bob[i])^vec[i]^int(key_BE[i]))
CBC_decoded_bob =[]
CBC_decoded_bob.append(helper_str)
helper_str =""
j =0
for block in CBC_encoded_to_bob:
    if j>0:
        cipher_block = CBC_encoded_to_bob[j-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_BE[i]))
        CBC_decoded_bob.append(helper_str)
        helper_str = ""
    j+=1
#Bob decoding to text
CBC = ""
for block in CBC_decoded_bob:
    CBC += chr(int(block, 2))
print("in the end bob recieved '" + CBC + "' using CBC")

#-------CFB----------
#alice is coding the message
bit_CFB = copy.deepcopy(message_binary)
block1_CFB = bit_CFB[0]
for i in range(8):
    helper_str+= str(vec[i]^int(key_AE[i])^int(block1_CFB[i])) #XOR first block
bit_CFB[0] = helper_str
CFB_encoded =[]
CFB_encoded.append(helper_str)
helper_str = ""
j = 0
for block in bit_CFB:
    if j>0:
        cipher_block = CFB_encoded[j-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_AE[i]))
        CFB_encoded.append(helper_str)
        helper_str = ""
    j+=1
    
# eve is decoding using Alice-Eve key
block1_eve_CFB = CFB_encoded[0]
for i in range(8):
    helper_str += str(int(block1_eve_CFB[i])^vec[i]^int(key_AE[i]))
CFB_decoded_eve =[]
CFB_decoded_eve.append(helper_str)
helper_str = ""
g = 0
for block in CFB_encoded:
    if g>0:
        cipher_block =  CFB_encoded[g-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_AE[i]))
        CFB_decoded_eve.append(helper_str)
        helper_str =""
    g+=1
    
# eve is coding using Bob_Eve key and sends the message to bob
block1_eve_bob = CFB_decoded_eve[0]
for i in range(8):
    helper_str+= str(int(block1_eve_bob[i])^vec[i]^int(key_BE[i])) #XOR first block
CFB_decoded_eve[0] = helper_str
CFB_encoded_to_bob =[]
CFB_encoded_to_bob.append(helper_str)
helper_str = ""
j = 0
for block in CFB_decoded_eve:
    if j>0:
        cipher_block = CFB_encoded_to_bob[j-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_BE[i]))
        CFB_encoded_to_bob.append(helper_str)
        helper_str = ""
    j+=1
    
#bob is decoding recieved message using bob-eve key
block1_bob = CFB_encoded_to_bob[0]
for i in range(8):
    helper_str += str(int(block1_bob[i])^vec[i]^int(key_BE[i]))
CFB_decoded_bob =[]
CFB_decoded_bob.append(helper_str)
helper_str =""
j =0
for block in CFB_encoded_to_bob:
    if j>0:
        cipher_block = CFB_encoded_to_bob[j-1]
        for i in range(8):
            helper_str += str(int(block[i])^int(cipher_block[i])^int(key_BE[i]))
        CFB_decoded_bob.append(helper_str)
        helper_str = ""
    j+=1
#Bob decoding to text
CFB = ""
for block in CFB_decoded_bob:
    CFB += chr(int(block, 2))
print("in the end bob recieved '" + CBC + "' using CFB")


