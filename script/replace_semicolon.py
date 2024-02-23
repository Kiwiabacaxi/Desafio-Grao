# path
path = './data/commerce_dataset.csv'

# Abra o arquivo em modo de leitura
# with open('seu_arquivo.csv', 'r') as file:
with open(path, 'r') as file:
    # Leia o conteúdo do arquivo
    file_data = file.read()

# Substitua todos os ';' por ','
file_data = file_data.replace(';', ',')

# Abra o arquivo em modo de gravação
# with open('seu_arquivo.csv', 'w') as file:
with open(path, 'w') as file:
    # Escreva o novo conteúdo no arquivo
    file.write(file_data)