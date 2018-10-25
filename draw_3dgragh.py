import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def func(delta, k):
    return delta ** k * (3 - delta) - 5 * (1 - delta) - delta ** 201


def main():
    count = 0
    deltas = np.arange(0.01, 1, 0.01)
    ks = np.arange(0, 200, 1)
    X = []
    Y = []
    Z = []
    for d in deltas:
        for k in ks:
            v = func(d, k)
            # X.append(d)
            # Y.append(k)
            # Z.append(v)
            if v > 0:
                X.append(d)
                Y.append(k)
                Z.append(v)
                # print("Delta: {:.2f} k: {} Result: {:.2f}".format(d, k, v))
                # count += 1

    # X, Y = np.meshgrid(x, y)
    # print(count)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel("Deltas")
    ax.set_ylabel("k")
    ax.set_zlabel("Result")

    ax.scatter(X, Y, Z, s=1)
    plt.show()

if __name__ == '__main__':
    main()
