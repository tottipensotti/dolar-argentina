import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_env()
tokenBCRA = os.getenv("tokenBCRA") # Es necesario generar un token de acceso
urlBCRA = 'https://api.estadisticasbcra.com/usd_of'
urlDolarApi = 'https://dolarapi.com/v1/dolares'

def getBcraData(url, token):
    r = requests.get(url, headers={
        'Authorization':f'BEARER {token}'
    })

    data = r.json()

    dolarOficial = (pd.DataFrame(data)
                    .rename(columns={'d':'Fecha', 'v':'Cotizacion'})
                    .sort_values(by='Fecha', ascending=False))
    
    return dolarOficial

def getDolarData(url):
    r = requests.get(url)
    data = r.json()
    
    cotizaciones = []
    
    for i in range(0, len(data)):
        cotizaciones.append([
            data[i]['nombre'],
            data[i]['compra'],
            data[i]['venta'],
            datetime.strptime(data[i]['fechaActualizacion'],"%Y-%m-%dT%H:%M:%S.%fZ")+ timedelta(hours=-3)
        ])

    cotizacionesDolar = pd.DataFrame(cotizaciones, columns=['tipo_dolar', 'compra', 'venta', 'fecha'])
    return cotizacionesDolar


if __name__ == '__main__':
    getBcraData(urlBCRA, tokenBCRA)
    getDolarData(urlDolarApi)