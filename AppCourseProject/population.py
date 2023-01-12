def Get_Population():
    Keys = ['Colombia', 'Mexico', 'United States','Japan','Russia']
    Values = [51,130,331,125,143]
    return Keys, Values

A = 'Hi'

def population_by_country(data, country):
    result = list(filter(lambda item: item['Country'] == country, data))
    return result
