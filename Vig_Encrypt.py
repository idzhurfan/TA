def vigenere(text, key):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            if any([i > 'z' or i < 'a' for i in key]):
                if any([i > 'Z' or i < 'A' for i in key]):
                    raise("Error: Please use character (A-Z) only in key")
            key_index += 1
            shift = ord(key_char.upper()) - ord('A')
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('A'))
        else:
            result += char
    return result
def text_to_bytes(text):
    return "".join(str(ord(char)) for char in text)

plain_text = input("Masukkan pesan informasi: ")
key = input("Masukkan kunci: ")

code_text = vigenere(plain_text, key)
codestream = text_to_bytes(code_text)

print("Codetext: ", code_text)
print("Index ASCII: ", codestream)
