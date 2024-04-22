def decode(message_file):
    with open(message_file, 'r') as file:
        lines = file.readlines()

    words_array = [0 for _ in range(len(lines))]

    # Iterate over each line in reverse order to decode the message
    for line in lines:

        words = line.strip().split()

        num = int(words[0])

        word = words[1]

        words_array[num - 1] = word

    decoded_message = ' '.join(words_array)
    
    return decoded_message

# Example usage:
decoded_message = decode('encoded_message.txt')
print(decoded_message)