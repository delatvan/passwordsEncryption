"""delatvan@gmail.com 
    26.06.2017
    """

import unittest
import os
import os.path
from secure import *

BLOCK_SIZE = 128
IV_SIZE = 16

class TestStringMethods(unittest.TestCase):

    def testHashingFLength(self):
    	password = "Ola324"
    	key = hashingF(password)
        self.assertEqual(32, len(key))

    def testPadders(self):
    	text = "Hola"
    	paddedData = paddingF(text,BLOCK_SIZE)
    	data = unpaddingF(paddedData,BLOCK_SIZE)
    	self.assertEqual(text,data)

    def test_EncriptionFuncs16Text(self):
    	password = "Foo33"
    	text = "PyGotham16Crypto"
    	iv = os.urandom(IV_SIZE)
    	key = hashingF(password)
    	ciphertext = encryptingF(key,iv,text)
    	plaintext = decryptingF(key,iv,ciphertext)
        self.assertEqual(text,plaintext)

    def test_EncriptionFuncsNot16Text(self):
    	password = "Benvenuto123.._2"
    	text = "Hola98"
    	iv = os.urandom(IV_SIZE)
    	key = hashingF(password)
    	ciphertext = encryptingF(key,iv,paddingF(text,BLOCK_SIZE))
    	plaintext = decryptingF(key,iv,ciphertext)
    	data = unpaddingF(plaintext,BLOCK_SIZE)
        self.assertEqual(text,data)

    def test_EncriptionFiles(self):
    	password = "HolaAmigo123"
    	fileName = "passwordsExample"
    	key = hashingF(password)
    	encryptingFile(fileName,key)
    	decryptingFile(fileName+"Encrypted",key)
    	fileReaderOriginal = open(fileName,"r")
    	fileReaderDeciphered = open(fileName+"Decrypted","r")
    	passwordOriginal = fileReaderOriginal.next()
    	fileReaderDeciphered.next()
    	passwordDeciphered = fileReaderDeciphered.next()
    	self.assertEqual(passwordOriginal,passwordDeciphered)
        fileReaderOriginal.close()
        fileReaderDeciphered.close()

    def test_OnAlreadyEncryptedFiles(self):
    	password = "GoTHoCBBBM"
    	fileName = "passwordsExampleDecrypted"
    	key = hashingF(password)
    	encryptingFile(fileName,key) #generates passwordsExampleEncrypted file
    	decryptingFile("passwordsExampleEncrypted",key) #generates again passwordsExampleDecrypted
    	self.assertTrue(os.path.isfile(fileName))
    	self.assertTrue(os.path.isfile("passwordsExampleEncrypted"))
    	

if __name__ == '__main__':
    unittest.main()