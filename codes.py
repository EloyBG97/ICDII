import csv

def __read_code(filename):
    dict = {}

    with open(filename,'r',encoding='UTF8') as f:
        reader = csv.reader(f, delimiter=';')

        for row in reader:
            code = row[0]
            name = row[1]

            dict[code] = name

    return dict


def __read_code_unit(filename):
    dict = {}

    with open(filename,'r',encoding='UTF8') as f:
        reader = csv.reader(f, delimiter=';')

        for row in reader:
            code = row[0]
            name = row[1]
            symbol = row[2]
            unit = row[3]

            dict[code] = {
                'name': name,
                'symbol': symbol,
                'unit': unit
            }

    return dict

def provincias():
    return __read_code('provincias.csv')

def municipios():
    dict = {}

    with open('20codmun.csv','r',encoding='UTF8') as f:
        reader = csv.reader(f, delimiter=';')

        for row in reader:
            autonoma = row[0]
            provincia = row[1]
            municipio = row[2]
            nombre = row[3]


            dict[provincia + '.' + municipio] = {
                'autonoma': autonoma,
                'provincia': provincia,
                'municipio': municipio,
                'nombre': nombre
            }

    return dict

def comunidad_autonoma():
    return __read_code('comautonoma.csv')


def contaminantes():
    return __read_code_unit('contaminantes.csv')
