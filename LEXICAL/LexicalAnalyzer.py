# Define characters
Alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
Capital_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
Small_letters = set('abcdefghijklmnopqrstuvwxyz')
Digits = set('0123456789')
Integers = Digits | {'-'}
Special_characters = set('.+-*/%<>=\'",;|!()[]_^~& ')
Underscore = {'_'}

# Define sets
Character = Alphabet | Digits | Special_characters
Alphabet = Capital_letters | Small_letters
Special_Characters = set('.+-*/%<>=\'",;|!()[]_^~& ')

# Define keywords and reserved words
Keywords = {'IF', 'ELSE', 'WHILE', 'FOR', 'INT', 'FLOAT', 'CHAR', 'RETURN', 'BREAK'}

# Check if an identifier is valid based on the given rules
def is_valid_identifier(identifier):
    if not identifier or identifier[0] not in Alphabet | Underscore:
        return False

    for char in identifier[1:]:
        if char not in Alphabet | Digits | {'-', '_'}:
            return False

    return identifier.upper() not in Keywords

# Test the validity of identifiers
identifiers = ['variable', '_Variable', '123Var', 'KeyWord', 'IF', 'FirstName', 'firstName']
for identifier in identifiers:
    print(f"{identifier} is {'valid' if is_valid_identifier(identifier) else 'invalid'} identifier.")
