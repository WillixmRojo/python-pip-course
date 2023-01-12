def Get_Population(Country):
    PopulationDictionary = {
        '2022': int(Country['2022 Population']),
        '2020': int(Country['2020 Population']),
        '2015': int(Country['2015 Population']),
        '2010': int(Country['2010 Population']),
        '2000': int(Country['2000 Population']),
        '1990': int(Country['1990 Population']),
        '1980': int(Country['1980 Population']),
        '1970': int(Country['1970 Population'])
    }

    Labels = PopulationDictionary.keys()
    Values = PopulationDictionary.values()
    
    return Labels, Values

def population_by_country(Data, Country):
    Result = list(filter(lambda item: item['Country/Territory'] == Country, Data))
    return Result