import matplotlib.pyplot as pyplot

def generate_pie_chart():
    Labels = ['A','B','C']
    Values = [100,200,300]

    fig, ax = pyplot.subplots()
    ax.pie(Values, labels = Labels)
    pyplot.savefig('pie.png')
    pyplot.close()
