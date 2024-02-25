path = './data/commerce_dataset.csv'

# Abra o arquivo em modo de leitura
with open(path, 'r') as file:
    file_data = file.read()

file_data = file_data.replace(';', ',')

# Abra o arquivo em modo de gravação
with open(path, 'w') as file:
    file.write(file_data)