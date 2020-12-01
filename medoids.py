import matplotlib.pyplot as plt
import random
import math
from collections import defaultdict


# vypocita vzdialenost medzi jednym bodom a medoidom
def vzdialenost(p1, p2):
    d = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return d


# najde najblizsi centroid k danemu bodu
def najdi_naj_medoid(distance):
    # najde najmensiu value v dictionary a vrati key tejto value
    mini = min(distance.keys(), key=(lambda k: distance[k]))
    return mini


def cena(klastre, medoids):
    cena = 0
    # for each cluster add distance between sample and medoid as cost


def vytvor_klastre(priestor, medoids):
    klastre = []
    for i in range(0, 20):
        klastre = defaultdict(list)
        for point in priestor:
            distance = {}
            index_m = 0
            for m in medoids:
                # vyratame vzdialenost bodu od kazdeho medoidu
                distance[index_m] = vzdialenost(point, m)
                index_m += 1
            # vrati index medoidu, ktoru mal najmensiu vzdialost od toho bodu
            vysledny = najdi_naj_medoid(distance)
            # dictionary, kde key je klaster a values su body, ktore boli vyhodnotene ako najblizsie k tomu centroidu
            klastre[vysledny].append(point)
    return klastre

if __name__ == '__main__':
    random.seed(a=None, version=2)
    priestor = []
    # Return a k length list of unique elements chosen from the population sequence or set. Used for random sampling without replacement.
    x = random.sample(range(-5000, 5000), k=20)
    y = random.sample(range(-5000, 5000), k=20)
    for i, j in zip(x, y):
        priestor.append((i, j))

    fig = plt.figure(figsize=(16.5, 9))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    for i in range(0, 40000):
        random_bod = random.randint(0, len(priestor) - 1)
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        nove_x = priestor[random_bod][0] + x_offset
        nove_y = priestor[random_bod][1] + y_offset
        priestor.append((nove_x, nove_y))

    k = 10

    medoids = random.sample(priestor, k=k)
    vzdialenosti = []

    for c in priestor:
        ax2.plot(c[0], c[1], 'o', color='gray',
                 markersize=5, linewidth=1,
                 markerfacecolor='white',
                 markeredgecolor='gray',
                 markeredgewidth=1)

    for i in medoids:
        ax2.plot(i[0], i[1], 'ro')

    klastre = vytvor_klastre(priestor, medoids)

    # calculate initial cost between samples and medoids
    # iterate until we no longer have a cheaper cost
    # choose non medoid in cluster
    # calculate cost when swapping medoid and sample -
        # swap sample and medoid
        # assign samples to new medoids
        # calculate new cost
        # if the swap gives us lower cost, we save the medoids and cost


    colors = ['palegreen', 'gold', 'royalblue', 'darkorchid', 'orange', 'lightcoral', 'maroon', 'darkgoldenrod',
              'forestgreen', 'navajowhite', 'mediumturquoise', 'c', 'skyblue', 'slateblue', 'pink', 'teal', 'tomato', 'brown',
              'purple', 'dodgerblue'
              ]
    for k in range(0, k):
        for item in range(0, len(klastre[k])):
            ax1.plot(klastre[k][item][0], klastre[k][item][1], 'o', color=colors[k], markeredgecolor='black', markeredgewidth=1)

    for i in medoids:
        ax1.plot(i[0], i[1], 'ro')

    plt.show()
