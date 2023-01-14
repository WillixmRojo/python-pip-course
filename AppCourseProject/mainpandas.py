import charts
import pandas as pd

def run():

    Data = pd.read_csv('data.csv')

    Data = Data[Data['Continent'] == 'Africa']

    Country = Data['Country/Territory'].values
    Percentages = Data['World Population Percentage'].values

    charts.GeneratePieChart('Percentages', Country, Percentages)
    
if __name__ == '__main__':
    run()
    
#para poder correr en terminal cuando solo lo mandas a llamar
