import random
from collections import Counter

someWords = '''apple banana lemon mango strawberry grape orange pineapple
muskmelon lychee peach berry papaya cherry watermelon apricot'''

someWords = someWords.split(' ')

word = random.choice(someWords)
print(word)

if __name__ == '__main__':
    print('Guess the Word! HINT: Word is a fruit')

    for i in word:
        print('_',end = ' ')

    print()

    playing = True

    letterGuessed = ''
    chances = len(word) + 2
    correct = 0
    flag = 0

    try:
        while(chances!=0)and flag ==0:
            print()
            chances-=1

            try:
                guess = str(input('Enter a letter to guess: '))
            except:
                print('Enter only a letter!')
                continue

            # Validate the Guess made
            if not guess.isalpha():
                print('Enter only a LETTER')
                continue
            elif len(guess)>1:
                print('Enter only a SINGLE letter')
                continue
            elif guess in letterGuessed:
                print('you have already guessed that letter')
                continue

            # when the letter is guessed correctly
            if guess in word:
                k = word.count(guess)
                for _ in range(k):
                    letterGuessed += guess
            
            # printing the word
            for char in word:
                if char in letterGuessed and (Counter(letterGuessed) != Counter(word)):
                    print(char, end = ' ')
                    correct =+1
                elif(Counter(letterGuessed)==Counter(word)):
                    print('The word is:', end = ' ')
                    print(word)
                    flag = 1
                    print('Congratulations, You WON!!!')
                    break
                break
            else:
                print('_', end = ' ')
        
        # When the user has used all the chances
        if chances<=0 and (Counter(letterGuessed)!= Counter(word)):
            print()
            print('You LOST!! Try again.......')
            print('The word was {}'.format(word))
    
    except KeyboardInterrupt:
        print()
        print('BYE! Try again..')
        exit()
            