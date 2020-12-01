import matplotlib.pyplot as plt
import random
import math
from collections import defaultdict


# vypocita vzdialenost medzi jednym bodom a centroidom
def vzdialenost(p1, p2):
    d = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return d


# najde najblizsi centroid k danemu bodu
def najdi_naj_centroid(distance):
    # najde najmensiu value v dictionary a vrati key tejto value
    mini = min(distance.keys(), key=(lambda k: distance[k]))
    return mini

#Krok 1: Priradenie inštancií do klastrov – pre každú inštanciu sa nájde najbližšie
#centrum a do klastra prislúchajúceho tomuto centru sa inštancia priradí.

#Krok 2: Úprava centier – nové centrá sa vypočítajú ako priemery inštancií
#patriacich príslušnému klastru.

if __name__ == '__main__':
    random.seed(a=None, version=2)
    priestor = []
    # Return a k length list of unique elements chosen from the population sequence or set. Used for random sampling without replacement.
    x = random.sample(range(-5000, 5000), k=3)
    y = random.sample(range(-5000, 5000), k=3)
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

    k = 3

    # 20 pociatocnych nahodnych centroidov
    # hocijaký bod v intervale od -5000 +5000 !
    # pricom ked robime s medoidom, tak je stred jeden z danych bodov
    centroids = []
    x = random.sample(range(-5000, 5000), k=k)
    y = random.sample(range(-5000, 5000), k=k)
    for i, j in zip(x, y):
        centroids.append((i, j))
    #centroids = random.sample(priestor, k=k)
    vzdialenosti = []

    for c in priestor:
        ax2.plot(c[0], c[1], 'o', color='gray',
                 markersize=5, linewidth=1,
                 markerfacecolor='white',
                 markeredgecolor='gray',
                 markeredgewidth=1)

    for i in centroids:
        ax2.plot(i[0], i[1], 'ro')

    for i in range(0, 20):
        klastre = defaultdict(list)
        for point in priestor:
            distance = {}
            index_c = 0
            for c in centroids:
                # vyratame vzdialenost bodu od kazdeho centroidu
                distance[index_c] = vzdialenost(point, c)
                index_c += 1
            # vrati index centroidu, ktoru mal najmensiu vzdialost od toho bodu
            vysledny = najdi_naj_centroid(distance)
            # dictionary, kde key je klaster a values su body, ktore boli vyhodnotene ako najblizsie k tomu centroidu
            klastre[vysledny].append(point)
            # prepisat centroidy - suradnica bude priemer - suma / pocet bodov v klastri
        #print(klastre)
        for i in range(0, len(klastre)):
            x = 0
            y = 0
            #print(len(klastre[i]))
            for j in range(0, len(klastre[i])):
                x += klastre[i][j][0]
                y += klastre[i][j][1]
            if len(klastre[i]) == 0:
                continue
            x /= len(klastre[i])
            y /= len(klastre[i])
            centroids[i] = (x, y)
    #print(centroids)

    colors = ['palegreen', 'gold', 'royalblue', 'darkorchid', 'orange', 'lightcoral', 'maroon', 'darkgoldenrod',
              'forestgreen', 'navajowhite', 'mediumturquoise', 'c', 'skyblue', 'slateblue', 'pink', 'teal', 'tomato', 'brown',
              'purple', 'dodgerblue'
              ]
    for k in range(0, k):
        for item in range(0, len(klastre[k])):
            ax1.plot(klastre[k][item][0], klastre[k][item][1], 'o', color=colors[k], markeredgecolor='black', markeredgewidth=1)

    for i in centroids:
        ax1.plot(i[0], i[1], 'ro')

    plt.show()
