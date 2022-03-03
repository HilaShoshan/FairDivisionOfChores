from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.simplefilter("ignore", UserWarning)


def draw_3D_triangle():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    triangle = np.array([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])

    ax.add_collection3d(Poly3DCollection(triangle, facecolors="white", linewidths=1, alpha=0.4))

    return fig, ax