import matplotlib.pyplot as plt
import random
import math
from collections import defaultdict
import threading
import heapq
from numba import jit

colors = ['crimson', 'coral', 'peachpuff', 'gold', 'orange', 'limegreen', 'darkgreen', 'deepskyblue', 'teal', 'navy', 'darkorchid', 'lightpink', 'deeppink',
          'lightgrey', 'slategray', 'royalblue', 'lightcyan', 'purple', 'darkgoldenrod', 'mintcream'
          ]


# vypocita vzdialenost medzi jednym bodom a centroidom
@jit(nopython=True)
def vzdialenost(p1, p2):
    d = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return d


def diviz(k, priestor):
    k_list = []
    x = 0
    y = 0
    centroids = []
    for point in priestor:
        x += point[0]
        y += point[1]
    x /= len(priestor)
    y /= len(priestor)
    max = -1
    farthest = priestor[0][0]
    for point in priestor:
        d = vzdialenost(point, (x, y))
        if d > max:
            max = d
            farthest = point

    centroids.append((x,y))
    centroids.append((farthest))
    klastre = vytvor_klastre(priestor, centroids)
    k_list.append(0)
    k_list.append(1)
    index_m = 2
    while len(klastre) < k:
        print(k)
        print(len(klastre))
        # find cluster with the largest diameter - maximum distance between two points
        max_diam = 0
        #max_klaster = klastre[0][0]
        for klaster in klastre:
            for i in range(0, len(klastre[klaster])):
                for j in range(i+1, len(klastre[klaster])):
                    d = vzdialenost(klastre[klaster][i], klastre[klaster][j])
                    if d > max_diam:
                        max_diam = d
                        max_klaster = klaster
        for i in range(0, len(klastre[max_klaster])):
            x += klastre[max_klaster][i][0]
            y += klastre[max_klaster][i][1]
        x /= len(klastre[max_klaster])
        y /= len(klastre[max_klaster])
        max = -1
        for point in range(0, len(klastre[max_klaster])):
            d = vzdialenost(klastre[max_klaster][point], (x, y))
            if d > max:
                max = d
                farthest = klastre[max_klaster][point]
        centroids.append((x, y))
        centroids.append((farthest))
        #centroids = [(x, y), (farthest)]
        #print(klastre[max_klaster])
        for point in klastre[max_klaster]:
            distance = {}
            index_c = index_m
            for c in range(index_m, len(centroids)):
                distance[index_c] = vzdialenost(point, centroids[c])
                index_c += 1
            vysledny = najdi_min(distance)
            klastre[vysledny].append(point)
            if vysledny not in k_list:
                k_list.append(vysledny)

        klastre.pop(max_klaster)
        k_list.remove(max_klaster)
        index_m += 2
    print(klastre)

    for k, j in zip(range(0, k), k_list):
        for item in range(0, len(klastre[j])):
            ax4.plot(klastre[j][item][0], klastre[j][item][1], 'o', color=colors[k], markeredgecolor='black', markersize=5,
                     markeredgewidth=1)
    #for i in centroids:
        #ax4.plot(i[0], i[1], 'ro')



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

    for k in range(0, k):
        for item in range(0, len(klastre[k])):
            ax1.plot(klastre[k][item][0], klastre[k][item][1], 'o', color=colors[k], markeredgecolor='black', markersize=5,
                     markeredgewidth=1)
    for i in centroids:
        ax1.plot(i[0], i[1], 'ro')


def cena(medoids, m, klastre):
    cena = 0
    for bod in klastre[m]:
        cena += vzdialenost(medoids[m], bod)
    return cena


# Update step: For each medoid m and each data point o associated to m swap m and o and compute the total cost of the configuration
# (that is, the average dissimilarity of o to all the data points associated to m). Select the medoid o with the lowest cost of the configuration.
def kmeans_medoid(k, priestor):
    # pociatocne medoidy
    medoids = random.sample(priestor, k=k)
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
                    # ak sme nasli lepsiu konfiguraciu
                    if cena_nova < cena_klastra:
                        cena_klastra = cena_nova
                        # zapamataj si novy medoid
                        naj_med = nove_medoidy
        if medoids == naj_med:
            break
        else:
            medoids = naj_med

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


def vzdialenost_centroid(klasterA, klasterB):
    if len(klasterA) == 1:
        centroidA = klasterA
    else:
        x = 0
        y = 0
        for i in range(0, len(klasterA)):
            x += klasterA[i][0]
            y += klasterA[i][1]
        x /= len(klasterA)
        y /= len(klasterA)
        centroidA = [(x, y)]

    if len(klasterB) == 1:
        centroidB = klasterB
    else:
        x = 0
        y = 0
        for i in range(0, len(klasterB)):
            x += klasterB[i][0]
            y += klasterB[i][1]
        x /= len(klasterB)
        y /= len(klasterB)
        centroidB = [(x, y)]

    d = math.sqrt((centroidA[0][0] - centroidB[0][0]) ** 2 + (centroidA[0][1] - centroidB[0][1]) ** 2)
    return d


def compute_distance(i, klaster_list, heap):
    j = i + 1
    klasterA = klaster_list[i]
    for k in range(j, len(klaster_list)):
        klasterB = klaster_list[k]
        distance = vzdialenost_centroid(klasterA, klasterB)
        heap_item = [distance, [klasterA, klasterB]]
        heapq.heappush(heap, heap_item)
    return heap


def setup(heap, klaster_list):
    for i in range(0, len(priestor)):
        heap = compute_distance(i, klaster_list, heap)
    return heap


def aglomer(k, priestor):
    heap = []
    klaster_list = []
    for i in range(0, len(priestor)):
        klaster_list.append([priestor[i]])
    heap = setup(heap, klaster_list)
    while len(klaster_list) > k:
        min_dist_klaster = heapq.heappop(heap)
        min_dist = min_dist_klaster[0]
        klasterA = min_dist_klaster[1][0]
        klasterB = min_dist_klaster[1][1]
        if klasterA in klaster_list and klasterB in klaster_list:
            klaster_list.remove(klasterA)
            klaster_list.remove(klasterB)
            klaster = klasterA + klasterB
            klaster_list.insert(0, klaster)
            heap = compute_distance(0, klaster_list, heap)

    for k in range(0, len(klaster_list)):
        for item in range(0, len(klaster_list[k])):
            ax3.plot(klaster_list[k][item][0], klaster_list[k][item][1], 'o', color=colors[k], markeredgecolor='black', markersize=6,
                     markeredgewidth=1)

    # distance between clusters
    # merge clusters with minimal distance


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

    for i in range(0, 100):
        random_bod = random.randint(0, len(priestor) - 1)
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        nove_x = priestor[random_bod][0] + x_offset
        nove_y = priestor[random_bod][1] + y_offset
        priestor.append((nove_x, nove_y))

    k = 15
    thread1 = threading.Thread(target=kmeans_centroid, args=(k, priestor))
    thread1.start()
    thread2 = threading.Thread(target=kmeans_medoid, args=(k, priestor))
    thread2.start()
    thread3 = threading.Thread(target=aglomer, args=(k, priestor))
    thread3.start()
    thread4 = threading.Thread(target=diviz, args=(k, priestor))
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    plt.show()
