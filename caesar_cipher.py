import string


def caesar(message, key):
    alphabet = string.ascii_lowercase + ' '
    letters = dict(enumerate(alphabet))
    coded_letters = {j: (i + key) % len(alphabet) for i, j in letters.items()}
    coded_message = ''
    for i in message:
        coded_message += letters[coded_letters[i]]
    return coded_message


text = input("Write the message to be coded:\n> ")
shift = int(input("Select key:\n> "))
print("Message:", text)
print("Key:", shift)
print("Coded message:", caesar(text, shift))
