# Define characters
Alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
Capital_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
Small_letters = set('abcdefghijklmnopqrstuvwxyz')
Digits = set('0123456789')
Integers = Digits | {'-'}
Special_characters = set('.+-*/%<>=\'",;|!()[]_^~& ')

# Define sets
Character = Alphabet | Digits | Special_characters
Alphabet = Capital_letters | Small_letters
Special_Characters = set('.+-*/%<>=\'",;|!()[]_^~& ')