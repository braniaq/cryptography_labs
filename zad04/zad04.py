#zad05
#Created by Jakub Branicki on 06/04/2020.

#modules
import math
import random
#functions
def generate_prime_numbers(range_max,quantity): #standard prime number generating algorithm
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
    primes= primes[half:] # so the numbers are bigger
    out=random.choices(primes, k= quantity) 
    return out

def generate_relatively_prime_number(range_min, range_max,pair):
    out =[]
    for i in range(range_max):
        if i>=range_min:
            ax = i
            bx = pair
            while(bx != 0):
                tmp = bx
                bx = ax%bx
                ax =tmp
            if ax ==1:
                out.append(i)
            half =int(len(out)/2)
            out = out[half:] # so the number is bigger
    return random.choice(out)

#RSA algorithm
rand_primes = generate_prime_numbers(25,2)
p = rand_primes[0]
q = rand_primes[1]
n = p*q
phi = (p-1)*(q-1)
e = generate_relatively_prime_number(2, phi, phi)
for i in range(n): #find d
    if ((i*e)%phi == 1):
        d=i

public_key = [n,e] #not needed
private_key = [n,d]

#read plain text
file = open('plaintext.txt')
data = file.read()
file.close()

#encryption
cipher=""
for c in data:
    x = ord(c)**e%n
    cipher += chr(x)

# write to file
file = open('ciphertext.txt', 'wb')
file.write(bytes(cipher, encoding= "utf-16")) 
file.close()

#read cipher
file =open('ciphertext.txt','rb')
encrypted_data = file.read()
encrypted_data = str(encrypted_data, "utf-16")
file.close()

#decryption
decrypted = ""
for c in encrypted_data:
    m = ord(c)**d%n
    decrypted+=chr(m)

#decrypted to file
file = open('decrypted_text.txt', 'w')
file.write("RSA\n"+ decrypted)
file.close()
