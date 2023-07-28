import csv

with open('exemplo_2.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["nome", "email", "telefone"])
    writer.writerow(["Jean", "jean@oi.com", "9170707070"])
    writer.writerow(["Jean", "jean@oi.com", "9170707070"])
    writer.writerow(["Jean", "jean@oi.com", "9170707070"])
    writer.writerow(["Jean", "jean@oi.com", "9170707070"])
