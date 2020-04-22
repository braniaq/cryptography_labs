from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16) # generate key

#read file
file = open("zerochain.txt", "r")
data = file.read()
file.close()

#encode data
helper_str = ""
data_bin = data.encode("utf-8")
endl = "\n".encode("utf-8")

cipher_ECB = AES.new(key, AES.MODE_ECB)
cipher_CBC = AES.new(key, AES.MODE_CBC)
cipher_CFB = AES.new(key, AES.MODE_CFB)

cfb_vec =cipher_CFB.iv #init vectors
cbc_vec = cipher_CBC.iv

#encryption
ciphertext_ECB = cipher_ECB.encrypt(data_bin)
ciphertext_CFB = cipher_CFB.encrypt(data_bin)
ciphertext_CBC = cipher_CBC.encrypt(data_bin)

#write file
file_w = open("encrypted.txt", "wb")
file_w.write(ciphertext_ECB)
file_w.write(endl)
file_w.write(ciphertext_CBC)
file_w.write(endl)
file_w.write(ciphertext_CFB)
file_w.close()
#read encrypted file
file = open("encrypted.txt", "rb")
coded =file.readlines()
file.close()
coded[0] = coded[0][:len(coded[0])-1] #clear new line chars
coded[1] = coded[1][:len(coded[1])-1]

decode_ECB = AES.new(key, AES.MODE_ECB)
decode_CBC = AES.new(key, AES.MODE_CBC, cbc_vec)
decode_CFB = AES.new(key, AES.MODE_CFB, cfb_vec)

#decryption
decrypted_ecb = decode_ECB.decrypt(coded[0])
decrypted_cbc = decode_CBC.decrypt(coded[1])
decrypted_cfb = decode_CFB.decrypt(coded[2])

#to file
file = open("decrypted.txt", "w")
file.write("ECB:\n")
file.write(str(decrypted_ecb)+"\n")
file.write("CBC:\n")
file.write(str(decrypted_cbc)+"\n")
file.write("CFB:\n")
file.write(str(decrypted_cfb)+"\n")