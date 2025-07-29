def make_hangman(secret_word):
    guesses = []
    
    def hangman_closure(letter):
        nonlocal guesses
        guesses.append(letter)
        
        display = ""
        for char in secret_word:
            if char in guesses:
                display += char
            else:
                display += "_"
        print(display)
        
        return all(char in guesses for char in set(secret_word))
    return hangman_closure
        
        
if __name__ == "__main__":
    print("Hangman!")
    secret = input("Enter the secret word: ").lower()
    
    guess_letter = make_hangman(secret)
    
    print("Enter letters here")
    while True:
        letter = input("Guess a letter: ").lower()
        if len(letter) != 1 or not letter.isalpha():
            print("Please enter a letter.")
            continue
        
        game_won = guess_letter(letter)
        if game_won:
            print(f"You did it! The word is '{secret}'.")
        break

    
    