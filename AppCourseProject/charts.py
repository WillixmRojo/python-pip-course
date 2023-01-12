import matplotlib.pyplot as plt

def GenerateBarChart(Name, Labels, Values):

    '''
    Labels = ['A','B','C']
    Values = [100,200,300]
    '''

    fig, ax = plt.subplots()

    ax.bar(Labels, Values)
    plt.savefig(f'./imgs/{Name}.png')
    plt.close()

def GeneratePieChart(Name, Labels, Values):

    fig, ax = plt.subplots()

    ax.pie(Values, labels = Labels)
    ax.axis('equal')
    plt.savefig(f'./imgs/{Name}.png')
    plt.close()

if __name__ == '__main__':
    
    Labels = ['William','Brandon','Mother']
    Values = [27,22,48]
    
    #Generates one, close to generate the other
    GenerateBarChart(Labels, Values)
    GeneratePieChart(Labels, Values)
