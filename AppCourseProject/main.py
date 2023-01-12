import utils
import read_csv
import charts

def run():

    Data = read_csv.read_csv('data.csv')

    Choice = int(input('Which would you like? \n 1.- Generate a bar chart for the population of a specific country. \n 2.- Generate a pie chart with the percentage of world population of every country. \n'))

    if Choice == 1:

        Country = input('What country would you like to see? ')

        Result = utils.population_by_country(Data, Country)

        if len(Result) > 0:
            Country = Result[0]
            Labels, Values = utils.Get_Population(Country)
            print(Result)
            charts.GenerateBarChart(Country['Country/Territory'], Labels, Values)

    if Choice == 2:    
        Percentages_Population = {item["Country/Territory"]: item["World Population Percentage"] for item in Data}

        Names = Percentages_Population.keys()
        Perc = Percentages_Population.values()
        charts.GeneratePieChart('Percentages', Names, Perc)

if __name__ == '__main__':
    run()
    
#para poder correr en terminal cuando solo lo mandas a llamar
    