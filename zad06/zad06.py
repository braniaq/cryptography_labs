#zad06
#Created by Jakub Branicki on 20/05/2020.

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
file = open('newplain.txt')
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

#zadanie NR 6<----------------------
file_stat = open('statistics.txt' , 'w')
cipher_list =[]
d = {}
prob = {}

for char in encrypted_data: # chars to list
    cipher_list.append(char) 
for char in cipher_list: #dictionary with char occurrence
    d[char] = cipher_list.count(char)
for char in cipher_list:
    prob[char] = cipher_list.count(char)/len(cipher_list) #dictionary with probability

entropy = 0

for char in prob: 
    entropy += prob[char] * math.log2(prob[char])
    
entropy *= -1  #Shannon entropy
metric_entropy = entropy/len(encrypted_data)


file_stat.write("\nentropy\n" + str(entropy) + "\n")
file_stat.write("\nmetric entropy\n" + str(metric_entropy) + "\n")
file_stat.write("char \t count\n" )
for char in d:
    file_stat.write(str(char) +"\t" + str(d[char]) + "\n")
    
file_stat.close()

