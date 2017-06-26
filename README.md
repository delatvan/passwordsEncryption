# delatvan@gmail.com
# 26.06.2017
# passwordsEncryption

Small script in python to cipher and decipher a text file containing passwords.

I do not claim responsibility for the use of the code. This is intended just as a practice of the pyca/cryptography package available for python.

There are three .py files contained in this project.

The first one is called secure.py:
This file contains all the necessary functions to cipher a file. 
hashingF is a hashing-function, which hashes a password of arbitrary length to a 256 key.
paddingF adds extra bytes "padding" to textblocks in order to always get 128 blocks.
encryptingF Uses the AES algorithm and a random generated Initialization value "iv" (to get a different
encryption each time the same word is encrypted).
encryptingFile which uses all the previously defined functions to encrypt a file. 

The second one is called secureTest.py:
It is a unittest to test all the functions used in secure.py

The third one is secureScript.py:
It is a user interface intended to be run in the terminal to help the user use the code of secure.py.
The code takes as an argument the name of the file to be encrypted. For example:
"python secureScript.py passwords"

#TODO: add decrption to files with extensions
