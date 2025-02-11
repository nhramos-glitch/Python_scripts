import random

choices = ('r', 'p', 's')
user_choice = input('Rock, Paper or scissors ? (r/p/s): ').lower()
if user_choice not in choices:
    print('Invalid choice!')
computer_choice = random.choice(choices)
print(f'You chose {user_choice}')
print(f'Computer choice {computer_choice}')