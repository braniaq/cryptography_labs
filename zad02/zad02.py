#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Fri Mar 27 21:46:13 2020
# @author: Jakub Branicki

#ECB x DES
#modules
import numpy as np
#permutation tables
entry_perm_table = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
sb1 = [[14,3,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]]
sb2 = [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]
sb3 = [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]]
sb4 = [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]
sb5 = [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]]
sb6 = [[12,1,10,15,9,2,6,7,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]]
sb7 = [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]]
sb8 = [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
pBox =[16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
key_table_1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
key_table_2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
extend_perm_table = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,28,28,29,30,31,32,1]
end_perm = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,36,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]

#functions
def permutation(before_perm, table):
    after_perm = np.zeros(len(table), dtype = int)
    for i in range(len(table)):
        after_perm[i] = before_perm[table[i]-1]
    return after_perm

def sbox(entry, box_table):
    out =[]
    row_list = [str(entry[0]),str(entry[5])]
    column_list = [str(entry[1]),str(entry[2]),str(entry[3]),str(entry[4]),]
    row_index= int(row_list[0]+row_list[1],2)
    column_index = int(column_list[0]+column_list[1]+column_list[2]+column_list[3],2)
    out_str = format(box_table[row_index][column_index], 'b')
    if len(out_str) != 4:
        out_str = out_str.rjust(4,"0")
    for i in range(len(out_str)):
        out.append(int(out_str[i]))
    return out

def move_key_left(key, quantity):
    out =[]
    for i in key:
        out.append(key[i-quantity])
    return out

#variables
cipher =[]
cipher_str =""
helper_list =[]
tmp = [] #helper
bit_msg_split =[]
helper_str = ""
message_binary = ""
key = np.random.randint(2,size= 64)
key_56b = permutation(key, key_table_1)

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
    tmp.append(int(message_binary[i]))
    if (i+1)%64 == 0:
        bit_msg_split.append(tmp)
        tmp = [] #clear() would break bit_msg_split
if len(tmp)!=0 :
    bit_msg_split.append(tmp)
last_block_index =len(bit_msg_split)-1
if len(bit_msg_split[last_block_index]) != 64: # fill last block with 0 if needed
    bit_msg_split[last_block_index] = bit_msg_split[last_block_index] + [0] * (64-len(bit_msg_split[last_block_index]))

#algorithm 
for block in bit_msg_split:
    block = permutation(block, entry_perm_table) #entry permutation
    left = block[0:32] #split sides
    right = block[32:64]
    key_56b = move_key_left(key_56b, 1) #move key by 1
    key_48b = permutation(key_56b, key_table_2) # new key
    right_extend = permutation(right, extend_perm_table) # extend permutation
    helper_list=[]
    helper_str=""
    six_bit_list =[]
    for i in range(48):
        helper_list.append(str(right_extend[i]^key_48b[i])) # XOR right side with key
    for i in range(48):
        helper_str += helper_list[i]
        if (i+1)%6 == 0:
            six_bit_list.append(helper_str)
            helper_str=""
    helper_list =[] #clear helper
    helper_list = sbox(six_bit_list[0],sb1) + sbox(six_bit_list[1],sb2) + sbox(six_bit_list[2],sb3) + sbox(six_bit_list[3],sb4) + sbox(six_bit_list[4],sb5) + sbox(six_bit_list[5],sb6) + sbox(six_bit_list[6],sb7) + sbox(six_bit_list[7],sb8) 
    after_box_list = permutation(helper_list, pBox) #pbox operation
    helper_list=[]
    new_right =[]
    new_left = right
    for i in range(32):
        new_right.append(after_box_list[i]^left[i]) #XOR new right side with left
    new_merged = list(new_left) + list(new_right) #merge left&right
    new_merged = permutation(new_merged,end_perm) # end permutation
    helper_str=""
    for i in range(64):
        helper_str += str(new_merged[i]) #out to string and list
    cipher.append(helper_str)
    cipher_str +=helper_str
    helper_str=""
#print
ciphers = ["EBC x DES:\n",cipher_str]
out_file = open("secured_zad02.txt","w")
out_file.writelines(ciphers)
out_file.close()