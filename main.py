import matplotlib.pyplot as plt
import random
import math
from collections import defaultdict
import threading
import numba
from numba import jit
from scipy.spatial import distance_matrix

colors = ['palegreen', 'gold', 'royalblue', 'darkorchid', 'orange', 'lightcoral', 'maroon', 'darkgoldenrod',
          'forestgreen', 'navajowhite', 'mediumturquoise', 'c', 'skyblue', 'slateblue', 'pink', 'teal', 'tomato',
          'brown',
          'purple', 'dodgerblue'
          ]


# vypocita vzdialenost medzi jednym bodom a centroidom
@jit(nopython=True)
def vzdialenost(p1, p2):
    d = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return d


def diviz(priestor, k):
    pass


# najde najblizsi centroid k danemu bodu
def najdi_min(distance):
    # najde najmensiu value v dictionary a vrati key tejto value
    mini = min(distance.keys(), key=(lambda k: distance[k]))
    return mini


def kmeans_centroid(k, priestor):
    # 20 pociatocnych nahodnych centroidov
    # hocijaký bod v intervale od -5000 +5000 !
    # pricom ked robime s medoidom, tak je stred jeden z danych bodov
    centroids = []
    x = random.sample(range(-5000, 5000), k=k)
    y = random.sample(range(-5000, 5000), k=k)
    for i, j in zip(x, y):
        centroids.append((i, j))
    # centroids = random.sample(priestor, k=k)
    vzdialenosti = []

   # for c in priestor:
       # ax2.plot(c[0], c[1], 'o', color='gray',
                # markersize=5, linewidth=1,
                # markerfacecolor='white',
                # markeredgecolor='gray',
                # markeredgewidth=1)

    #for i in centroids:
        #ax2.plot(i[0], i[1], 'ro')
    # Krok 1: Priradenie inštancií do klastrov – pre každú inštanciu sa nájde najbližšie
    # centrum a do klastra prislúchajúceho tomuto centru sa inštancia priradí.

    # Krok 2: Úprava centier – nové centrá sa vypočítajú ako priemery inštancií
    # patriacich príslušnému klastru.
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
            vysledny = najdi_min(distance)
            # dictionary, kde key je klaster a values su body, ktore boli vyhodnotene ako najblizsie k tomu centroidu
            klastre[vysledny].append(point)
            # prepisat centroidy - suradnica bude priemer - suma / pocet bodov v klastri
            # print(klastre)
        for i in range(0, len(klastre)):
            x = 0
            y = 0
            # print(len(klastre[i]))
            for j in range(0, len(klastre[i])):
                x += klastre[i][j][0]
                y += klastre[i][j][1]
            if len(klastre[i]) == 0:
                continue
            x /= len(klastre[i])
            y /= len(klastre[i])
            centroids[i] = (x, y)

    # print(centroids)
    for k in range(0, k):
        for item in range(0, len(klastre[k])):
            ax1.plot(klastre[k][item][0], klastre[k][item][1], 'o', color=colors[k], markeredgecolor='black', markersize=5,
                     markeredgewidth=1)
    for i in centroids:
        ax1.plot(i[0], i[1], 'ro')


def cena(medoids, m, klastre):
    cena = 0
    #for m in range(0, len(medoids)):
    for bod in klastre[m]:
        cena += vzdialenost(medoids[m], bod)
    return cena


# Update step: For each medoid m and each data point o associated to m swap m and o and compute the total cost of the configuration
# (that is, the average dissimilarity of o to all the data points associated to m). Select the medoid o with the lowest cost of the configuration.
def kmeans_medoid(k, priestor):
    # pociatocne medoidy
    medoids = random.sample(priestor, k=k)
    for i in medoids:
        ax3.plot(i[0], i[1], 'ro')
    # pociatocne klastre
    #klastre = vytvor_klastre(priestor, medoids)
    # m_klastre =
    # pociatocna cena
    #total_cost = cena(medoids, klastre)
    while True:
        klastre = vytvor_klastre(priestor, medoids)
        naj_med = medoids
        # for each medoid m
        for m in range(0, len(medoids)):
            nove_medoidy = naj_med.copy()
            cena_klastra = cena(nove_medoidy, m, klastre)
            # for each data point associated to m
            for bod in klastre[m]:
                if bod != nove_medoidy[m]:
                    # swap m and datapoint
                    nove_medoidy[m] = bod
                    # compute total cost of the configuration
                    cena_nova = cena(nove_medoidy, m, klastre)
                    if cena_nova < cena_klastra:
                        cena_klastra = cena_nova
                        # zapamataj si novy medoid
                        naj_med = nove_medoidy
        if medoids == naj_med:
            break
        else:
            medoids = naj_med



            # select medoid -bod- with the lowest cost of the configuration


    #for i in range(0, 5):
        #naj_medoidy = medoids
        #najnizsi_cost = total_cost
        #for m in medoids:
            #for bod in priestor:
                #print(total_cost)
                #if bod not in medoids:
                    #nove_medoidy = medoids.copy()
                    #print(nove_medoidy[m == medoids])
                    #nove_medoidy[m == medoids] = bod

                    #nove_klastre = vytvor_klastre(priestor, nove_medoidy)
                    #nova_cena = cena(nove_medoidy, nove_klastre)
                    #if nova_cena < najnizsi_cost:
                        #najnizsi_cost = nova_cena
                        #naj_medoidy = nove_medoidy
                #print(total_cost)
        # zapamataj si swap, ktory dal najnizsi cost
        #if najnizsi_cost < total_cost:
            #print(total_cost)
            #total_cost = najnizsi_cost
            #medoids = naj_medoidy
        #else:
            #break

    nove_klastre = vytvor_klastre(priestor, medoids)
    for k in range(0, k):
        for item in range(0, len(nove_klastre[k])):
            ax2.plot(nove_klastre[k][item][0], nove_klastre[k][item][1], 'o', color=colors[k], markeredgecolor='black', markersize=6,
                     markeredgewidth=1)
    for i in medoids:
        ax2.plot(i[0], i[1], 'ro')


def vytvor_klastre(priestor, medoids):
    klastre = defaultdict(list)
    for point in priestor:
        distance = {}
        index_m = 0
        for m in medoids:
            distance[index_m] = vzdialenost(point, m)
            index_m += 1
        vysledny = najdi_min(distance)
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

    fig = plt.figure(figsize=(12.8, 9.6))
    ax1 = fig.add_subplot(221)
    ax1.title.set_text('K-Means Centroid')
    ax2 = fig.add_subplot(222)
    ax2.title.set_text('K-Means Medoid')
    ax3 = fig.add_subplot(223)
    ax3.title.set_text('Aglomerativne zhlukovanie')
    ax4 = fig.add_subplot(224)
    ax4.title.set_text('Divizivne zhklukovanie')

    for i in range(0, 40000):
        random_bod = random.randint(0, len(priestor) - 1)
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        nove_x = priestor[random_bod][0] + x_offset
        nove_y = priestor[random_bod][1] + y_offset
        priestor.append((nove_x, nove_y))

    k = 10
    thread1 = threading.Thread(target=kmeans_centroid, args=(k, priestor))
    thread1.start()
    thread2 = threading.Thread(target=kmeans_medoid, args=(k, priestor))
    thread2.start()
    thread1.join()
    thread2.join()
    #kmeans_centroid(k, priestor)
    #kmeans_medoid(k, priestor)
    #aglomer()
    #diviz()

    plt.show()
