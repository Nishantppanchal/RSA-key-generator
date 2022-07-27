import random
from math import floor, sqrt, ceil, gcd, lcm
import sys
from numpy import number
import numpy as np
import os
import pickle

def bits_to_file_name(bits):
    return f'{bits}bitsPrimes'

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def generate_primes(start, limit):
    print('Generating prime numbers')
    case1 = [1, 13, 17, 29, 37, 41, 49, 53]
    case2 = [7, 19, 31, 43]
    case3 = [11, 23, 47, 59]

    primes = []
    # sieveList = [False] * limit
    sieveList = np.full(limit, False, dtype=bool)
    sieveList[1] = True
    sieveList[2] = True
    sieveList[4] = True

    printProgressBar(0, limit, prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    for n in range(1, limit + 1):
        r = n % 60
        
        printProgressBar(n , limit, prefix = 'Progress:', suffix = 'Complete', length = 50)

        if r in case1:
            xLimit = floor(sqrt(n) / 2)
            for x in range(1, xLimit + 1):
                y = sqrt((n - 4 * (x ** 2)))
                if y.is_integer():
                    sieveList[n - 1] = not sieveList[n - 1]
        if r in case2:
            xLimit = floor(sqrt(n / 3))
            for x in range(1, xLimit + 1):
                y = sqrt((n - 3 * (x ** 2)))
                if y.is_integer():
                    sieveList[n - 1] = not sieveList[n - 1]
        if r in case3:
            xLowerLimit = ceil(sqrt(n / 3))
            xUpperLimit = floor(sqrt(n / 2))
            for x in range(xLowerLimit, xUpperLimit + 1):
                y = sqrt((3 * (x ** 2) - n))
                if y.is_integer():
                    sieveList[n - 1] = not sieveList[n - 1]

    print('done')
    for n in range(1, limit + 1):
        if sieveList[n - 1] == True:
            if n >= start:
                primes.append(n)
            for m in range(n ** 2, limit + 1):
                if m % n == 0:
                    sieveList[m - 1] = False

    return primes

# Algorithm to generate keys manually using prime numbers


def generate_key_with_custom_RSA_algorithm(bits):

    # Creates numFrom and numTo, which are used in the for loop to test for prime numbers
    numFrom = int(2**((bits-1)/2))
    numTo = int(2**(bits/2))

    fileName = bits_to_file_name(bits)
    if os.path.exists(fileName):
        with open(fileName, 'rb') as file:
            primeNumberList = pickle.load(file)
    else: 
        primeNumberList = generate_primes(numFrom, numTo)
        with open(fileName, 'wb') as file:
            pickle.dump(primeNumberList, file)

    print('Calculating RSA keys')
    # Random prime numbers from prime file
    p = random.choice(primeNumberList)
    q = random.choice(primeNumberList)
    print(p, q)

    # gets the n value
    n = p*q

    # Computes λ(n) where λ is Carmichael's totient function
    λ = lcm(p-1, q-1)

    d = 0
    e = 0

    eFound = False
    while not eFound:
        e = random.randint(2, λ - 1)
        if gcd(e, λ) == 1:
            eFound = True

    d = pow(e, -1, λ)

    # Return keys as tuple: (e,d,n)
    return e, d, n, λ


def find_max_char_per_block(n):
    maxCharPerBlock = 0
    maxValue = '256'
    while int(maxValue) < n:
        maxCharPerBlock += 1
        maxValue += '256'
    return maxCharPerBlock


def convert_to_int(string, n, maxCharPerBlock):
    numberArray = []

    for i in range(0, len(string), maxCharPerBlock):
        stringSegment = string[i: i + maxCharPerBlock]
        currentNumber = ''
        for char in stringSegment:
            ASCIIStr = str(ord(char))
            while len(ASCIIStr) != 3:
                ASCIIStr = '0' + ASCIIStr

            currentNumber += ASCIIStr

        numberArray.append(currentNumber)

    return numberArray


def encrypt(blocks, n, e, maxCharPerBlock):
    cArray = []
    for m in blocks:
        m = int(m)
        c = pow(m, e, n)
        cArray.append(str(c))

    encryptedText = ' '.join(cArray)
    return encryptedText


def decrypt(message, n, d):
    cArray = message.split(' ')
    mArray = []
    for c in cArray:
        c = int(c)
        m = pow(c, d, mod=n)
        mArray.append(m)

    return mArray


def convert_to_char(blocks):
    text = ''
    for block in blocks:
        blockStr = str(block)
        while len(blockStr) % 3 != 0:
            blockStr = '0' + blockStr
        for i in range(0, len(blockStr) - 1, 3):
            subBlockInt = int(blockStr[i: i + 3])
            text += chr(subBlockInt)
    return text


def generate_keys_gui():
    print('#------Generating-Keys------#')
    bits = input("Enter Key Bits: ")
    # Issue with generating RSA keys
    e, d, n, λ = generate_key_with_custom_RSA_algorithm(int(bits))
    print(f'Public Key - e:{e} n:{n}')
    print(f'Private Key - d:{d} n:{n}')

    print(f'To verify the keys, d × e ≡ 1 mod λ(n)')
    print(f'Hence d × e - 1 mod λ(n) = 0 if the RSA keys are correct')
    print(f'In this case, d × e - 1 mod λ(n) = {(d * e - 1) % λ}')

    return e, d, n


def encrypt_message_gui(n, e):
    print('#------Encrypt-Message------#')
    maxCharPerBlock = find_max_char_per_block(n)
    message = input('Enter you message: ')
    blocks = convert_to_int(message, n, maxCharPerBlock)
    encryptedText = encrypt(blocks, n, e, maxCharPerBlock)
    print(f'Encrypted message: {encryptedText}')
    return encryptedText


def decrypt_message_gui(n, d, encryptedText):
    print('#------Decrypting-Message------#')
    decryptedBlocks = decrypt(encryptedText, n, d)
    text = convert_to_char(decryptedBlocks)
    print(f'Decrypted message: {text}')


if __name__ == "__main__":
    print('Menu Options:')
    print('1. Generate Key')
    print('2. Encrypt Message')
    print('3. Decrypt Message')
    print('4. Delete Primes Set')
    menuOption = input('Select a menu option: ')
    if menuOption == '1':
        e, d, n = generate_keys_gui()

        encryptedText = encrypt_message_gui(n, e)

        decrypt_message_gui(n, d, encryptedText)

    if menuOption == '2':
        print('Enter Public key components')
        e = int(input(' e: '))
        n = int(input(' n: '))

        encrypt_message_gui(n, e)

    if menuOption == '3':
        print('Enter Private key components')
        d = int(input(' d: '))
        n = int(input(' n: '))

        encryptedMessage = input('Enter the encrypted message: ')

        decrypt_message_gui(n, d, encryptedMessage)

    if menuOption == '4':
        print('#------Deleting-Primes-Set------#')
        bits = input("Enter Key Bits: ")
        fileName = bits_to_file_name(bits)
        os.remove(fileName)