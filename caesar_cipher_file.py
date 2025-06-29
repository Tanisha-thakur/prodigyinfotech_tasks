def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("File not found!")
        return ""

def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def main():
    print("=== Caesar Cipher with File Support ===")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").upper()
    input_file = input("Enter input file name (e.g., input.txt): ")
    output_file = input("Enter output file name (e.g., output.txt): ")
    shift = int(input("Enter shift value (0-25): "))

    message = read_file(input_file)
    if not message:
        return

    if choice == 'E':
        result = encrypt(message, shift)
    elif choice == 'D':
        result = decrypt(message, shift)
    else:
        print("Invalid choice.")
        return

    write_file(output_file, result)
    print(f"Operation completed! Check the file: {output_file}")

if __name__ == "__main__":
    main()
