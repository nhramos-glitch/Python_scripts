import maskpass

username = input('What is your username: ')
password = maskpass.askpass(prompt='Password: ', mask='#')

password_length = len(password)
hidden_password = '*' * password_length

print(f'{username}, your password {hidden_password} is {password_length} character long ')