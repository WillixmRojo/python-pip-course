import csv

def read_csv(Path):
    with open(Path,'r') as csvFile:
        Reader = csv.reader(csvFile, delimiter = ',') #delimiter is the separator, most cases a comma
        Header = next(Reader) #Column names
        #print(Header)
        Data = [] #create the array where we will store the data
        for Row in Reader:
            Iterable = zip(Header, Row) #melds column name with the row
            #print(list(Iterable))
            Country_Dictionary = {key: value for key, value in Iterable} #making the tuple with column name - row into a dictionary
            #print(Country_Dictionary)
            Data.append(Country_Dictionary)
    return Data

if __name__ == '__main__':
    Data = read_csv('data.csv')
    #print(Data[150])
