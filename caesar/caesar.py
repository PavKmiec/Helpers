# function to brute force caesar cipher



text = "uggc://64wzr446fuy7rbte.bavba/nffvfgnag.ugzy"



# function to brute force caesar cipher without having to know the key
def brute_force_caesar_cipher(text):
    for key in range(0,26):
        print(key)
        print(caesar_cipher(text, key))


# function to caesar cipher
def caesar_cipher(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - 65 + key) % 26 + 65)
            else:
                result += chr((ord(char) - 97 + key) % 26 + 97)
        else:
            result += char
    return result

brute_force_caesar_cipher(text)


