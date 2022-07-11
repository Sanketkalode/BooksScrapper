
def save_to_file(title, operation):
    with open('files/save.csv', mode='a') as file:
        file.write(str(title + ", " + operation) + '\n')





