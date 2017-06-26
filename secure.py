"""delatvan@gmail.com 
	27.06.2017
	"""

import sys
import os
from ast import literal_eval
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives import padding

BLOCK_SIZE = 128
Key_SIZE = 256
IV_SIZE = 16

def hashingF(password):
	"""Hashin function:
	Converts simple password into 256 hashKey"""
	digest = hashes.Hash(hashes.SHA256(),backend=default_backend())
	digest.update(password.encode('UTF-8'))
	key = digest.finalize()
	return key

def paddingF(text,blockSize):
	"""Padding function:
	Adds bytes to get blocks of size 128
	"""
	padder = padding.PKCS7(blockSize).padder()
	paddedData = padder.update(text)+padder.finalize()
	return paddedData

def unpaddingF(text, blockSize):
	"""Unpadding function:
	Inverse of paddingF. Takes away extra bytes
	"""
	unpadder = padding.PKCS7(blockSize).unpadder()
	data = unpadder.update(text)+unpadder.finalize()
	return data

def encryptingF(key, iv, plainText):
	""" Encryption function:
	Encrypts a string
	"""
	cipher = Cipher(algorithms.AES(key),modes.CBC(iv),
		backend = default_backend())
	encryptor = cipher.encryptor()
	cipher_text = encryptor.update(plainText) + encryptor.finalize()
	return cipher_text

def decryptingF(key, iv, cipherText):
	""" Decryption function:
	Decrypts a string
	"""
	cipher = Cipher(algorithms.AES(key),modes.CBC(iv),
	backend = default_backend())
	decryptor = cipher.decryptor()
	plaintext = decryptor.update(cipherText) + decryptor.finalize()
	return plaintext

def encryptingFile(fileName, key):
	""" Encryption of a file:
	Encrypts a whole file
	"""
	fileReader = open(fileName,"r")
	tmpList = fileName.split(".")
	fileName = tmpList[0]
	try:
		extension = "."+tmpList[1]
	except Exception,e:
		extension=""
		pass
	firstLine = fileReader.next().split("    ")
	#Case were file hasn't ever been encrypted by this program
	if firstLine[0]!= "decrypted file:":
		fileWriter = open(fileName+"Encrypted"+extension,"w")
		fileWriter.write("encrypted file:    "+fileName+extension+"    \n")
		fileReader.seek(0)
	#Case were file was already encrypted by the program
	else:
		tmpList = firstLine[1].split(".")
		try:
			extension = "."+tmpList[1]
		except Exception,e:
			extension=""
			pass
		fileWriter = open(tmpList[0]+"Encrypted"+extension,"w")
		fileWriter.write("encrypted file:    "+tmpList[0]+extension+"    \n")
	for line in fileReader:
		iv = os.urandom(IV_SIZE)
		cipherText = encryptingF(key,iv,paddingF(line,BLOCK_SIZE))
		fileWriter.write(repr(cipherText)+"    "+repr(iv)+"    \n")
	fileWriter.flush()
	os.fsync(fileWriter)
	fileWriter.close()
	fileReader.close()
	print "Your file is encrypted"	

def decryptingFile(fileName, key):
	fileReader = open(fileName,"r")	
	firstLine = fileReader.next().split("    ")
	if firstLine[0]!= "encrypted file:":
		raise ValueError("\nThis file hasn't been encrypted before\n")
		fileReader.close()
		sys.exit()
	tmpList = firstLine[1].split(".")
	try:
		extension = "."+tmpList[1]
	except Exception,e:
		extension=""
		pass
	fileWriter = open(tmpList[0]+"Decrypted"+extension,"w")
	fileWriter.write("decrypted file:    "+tmpList[0]+extension+"    \n")
	for line in fileReader:
		lineList = line.split("    ")
		cipherText = literal_eval(lineList[0])
		iv =  literal_eval(lineList[1])
		plaintext = decryptingF(key,iv,cipherText)
		fileWriter.write(unpaddingF(plaintext,BLOCK_SIZE))
	fileWriter.flush()
	os.fsync(fileWriter)
	fileWriter.close()
	fileReader.close()
	print "Your file is decrypted"
