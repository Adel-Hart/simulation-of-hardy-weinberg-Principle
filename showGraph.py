import matplotlib.pyplot as plt
import matplotlib
import numpy

plt.ion()
x = numpy.arange(3)

def showGraph(entities : list, pos : tuple):

    horiz = ["AA", "Aa(aA)", "aa"]
    vertic = []

    AA = 0
    aa = 0
    Aa = 0


    for i in entities:
        gene = i.gene
        resGene = ''.join(gene)

        if resGene == "AA":
            AA += 1
        elif resGene == "aa":
            aa += 1
        else:
            Aa += 1
    

    vertic = [AA, Aa, aa]

    plt.figure(num=1, figsize=[pos[0], pos[1]])



    plt.bar(x, vertic, align='edge', edgecolor = 'lightgray', linewidth=3, color = ['r', 'g', 'b'])
    plt.xticks(x, horiz)

    plt.show()
    plt.pause(0.2)
    plt.clf()
