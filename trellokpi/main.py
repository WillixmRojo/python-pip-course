import pandas as pd
import matplotlib as plt2
import matplotlib.pyplot as plt
import charts

plt2.use('Agg')

Data_TrelloBoard = pd.read_csv('TARJETAS TRELLO.csv')

BoardName = 'GCIA Operación Retail y Servicios Financieros, Inmobiliaria, Diseño y Construcción'
FilterBoard = Data_TrelloBoard[Data_TrelloBoard['board_name'] == BoardName]

Grouped = FilterBoard.groupby(['member_fullName']).size()

Grouped.plot(kind='bar')

plt.xlabel('Member Name')
plt.ylabel('Count')

plt.subplots_adjust(bottom=0.75)

plt.savefig('plot.png')



#charts.GenerateBarChart(Label, Value)