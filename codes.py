import csv

def __read_code(filename):
    dict = {}

    with open(filename,'r',encoding='UTF8') as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            code = row[0]
            name = row[1]

            dict[code] = name

    return dict


def __read_code_unit(filename):
    dict = {}

    with open(filename,'r',encoding='UTF8') as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            code = row[0]
            name = row[1]
            magnitude = int(row[2])

            dict[code] = (name, 1/magnitude)

    return dict

def provincias():
    return __read_code('provincias.csv')

def municipios():
    return __read_code('municipios.csv')

def contaminantes():
    return __read_code_unit('contaminantes.csv')
