import matplotlib.pyplot as plt
import random

if __name__ == '__main__':
    random.seed(a=None, version=2)
    priestor = []
    # Return a k length list of unique elements chosen from the population sequence or set. Used for random sampling without replacement.
    x = random.sample(range(-5000, 5000), k=20)
    y = random.sample(range(-5000, 5000), k=20)
    for i, j in zip(x, y):
        priestor.append((i, j))

    fig = plt.figure(figsize=(9, 9))
    ax1 = fig.add_subplot(111)

    for i in range(0, 40000):
        random_bod = random.randint(0, len(priestor)-1)
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        nove_x = priestor[random_bod][0] + x_offset
        nove_y = priestor[random_bod][1] + y_offset
        priestor.append((nove_x, nove_y))

    for c in priestor:
        #ax1.plot(c[0], c[1], color = ' gray')
        ax1.plot(c[0], c[1], 'o', color='gray',
                 markersize=5, linewidth=1,
                 markerfacecolor='white',
                 markeredgecolor='gray',
                 markeredgewidth=1)

    plt.show()
