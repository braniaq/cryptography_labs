#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Fri Mar 27 21:46:13 2020
# @author: Jakub Branicki

#modules
import numpy as np
import copy
#variables
key = np.random.randint(2,size= 64)
init_vector = np.random.randint(2,size= 64)
tmp =""
bit_msg_split =[]
helper_str=""
cipher = ""
cipher2 = ""
cipher_list2 =[]
cipher3 = ""
cipher_list3 = []
#program

##Open, read and convert text to binary
file  = open('notsecured.txt')
message = file.read()
file.close()
for i in message:
    helper_str = format(ord(i), 'b')
    if (len(helper_str) < 8):
        helper_str = helper_str.rjust(8,"0")
    message_binary += helper_str
    helper_str=""
##Split it into 64 bit blocks
for i in range(len(message_binary)):
    tmp += message_binary[i]
    if (i+1)%64 == 0:
        bit_msg_split.append(tmp)
        tmp=""
if tmp != "":
    bit_msg_split.append(tmp)
last_block_index =len(bit_msg_split)-1
if len(bit_msg_split[last_block_index]) != 64: # fill last block with 0 if needed
    bit_msg_split[last_block_index] = bit_msg_split[last_block_index].ljust(64,"0")

#----------ECB------------
for block in bit_msg_split:
    for i in range(64):
        cipher += str(int(block[i])^int(key[i]))

#----------CBC------------
bit_msg= copy.deepcopy(bit_msg_split) #for CFB
block1 = bit_msg_split[0]
for i in range(64):
    helper_str += str(int(block1[i])^int(init_vector[i])^int(key[i])) # XOR first block
bit_msg_split[0] = helper_str
cipher_list2.append(helper_str)
helper_str =""
cipher2= str(cipher_list2[0])
j = 0
for block in bit_msg_split: # rest of the blocks
    if j>0:
        cipher2_block = cipher_list2[j-1]
        for i in range(64):
            helper_str += str(int(block[i])^int(cipher2_block[i])^int(key[i]))
        cipher_list2.append(helper_str)
        cipher2 +=helper_str
        helper_str=""
    j+=1
#----------CFB------------
block1_CFB = bit_msg[0]
cipher_list3 = []
for i in range(64):
    helper_str += str(int(init_vector[i])^int(key[i])^int(block1_CFB[i])) #XOR first block
cipher_list3.append(helper_str)
helper_str = ""
cipher3 = cipher_list3[0]
k = 0
for block in bit_msg: # rest of the blocks
    if k>0:
        cipher3_block = cipher_list3[k-1]
        for i in range(64):
            helper_str += str(int(block[i])^int(cipher3_block[i])^int(key[i]))
        cipher_list3.append(helper_str)
        cipher3 += helper_str
        helper_str=""
    k+=1
# print
ciphers = ["EBC:\n",cipher,"\n","CBC:\n",cipher2,"\n","CFB:\n",cipher3,]
out_file = open("secured_zad01.txt","w")
out_file.writelines(ciphers)
out_file.close()