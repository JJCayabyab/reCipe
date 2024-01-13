def get_char_category(char):
    # Define character categories
    capital_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZÑNG")
    small_letters = set("abcdefghijklmnopqrstuvwxyzñngo")
    digits = set("0123456789")
    special_characters = set(".+-*/%<>=\",',;|!()[]_^~& ")

    # Check the category of the character
    if char in capital_letters:
        return "Capital_letter"
    elif char in small_letters:
        return "Small_letter"
    elif char in digits:
        return "Digit"
    elif char in special_characters:
        return "Special_character"
    else:
        return "Invalid_character"

# Example usage
input_string = "Hello123, 3.14 + World!"

for char in input_string:
    category = get_char_category(char)
    print(f"Character: {char}, Category: {category}")
