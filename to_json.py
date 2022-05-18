# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 13:31:33 2022

@author: eloyb
"""

import os
import csv
import codes
import json

dirname = './DATA/'
filenames = os.listdir(dirname)
jsons = []
_json = {}
provincias = codes.provincias()
municipios = codes.municipios()
comunidad_autonoma = codes.comunidad_autonoma()
contaminantes = codes.contaminantes()

for filename in filenames:
    with open(dirname + filename, 'r', encoding='UTF8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip the headers

        for row in reader:

            try:
                info_loc = municipios[row[0] + '.' + row[1]]
                
                cod_comunidad_autonoma = info_loc['autonoma']
                cod_provincia = info_loc['provincia']

                com_autonoma = comunidad_autonoma[cod_comunidad_autonoma]
                provincia = provincias[cod_provincia]
                municipio = info_loc['nombre']

                contaminante = contaminantes[row[3]]
                
                key = str(row[5]) + str(row[6] + str(provincia) + str(municipio) + str(row[2]))

                if(key in _json.keys()):
                    aux = _json[key]

                    data = {
                        'pollutant': contaminante[0]
                    }

                    for i in range(7, 38):
                        try:
                            data['D' + str(i - 6)] = float(row[i]) * contaminante[1]
                        except Exception:
                            None

                    aux['data'].append(data)
                    _json[key] = aux

                else:
                    aux = {
                        'location': {
                            'provincia': provincia,
                            'municipio': municipio,
                            'com_autonoma': com_autonoma,
                            'estacion': row[2]
                        },

                        'date': {
                            'month': int(row[6]),
                            'year': int(row[5])
                        },

                        'data': [
                            {
                                'pollutant': contaminante[0],
                            }
                        ]
                    }

                    for i in range(7, 38):
                        try:
                            aux['data'][-1]['D' + str(i - 6)] = float(row[i]) * contaminante[1]
                        except Exception:
                            None

                    _json[key] = aux

            except Exception:
                None


for key, value in _json.items():
    jsons.append(value)

x = json.dumps(jsons,ensure_ascii=False).encode('utf-8')

with open("data.json", "wb") as outfile:
    outfile.write(x)

    
    

