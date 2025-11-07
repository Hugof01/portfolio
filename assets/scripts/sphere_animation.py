import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class SphereAnimation:
    def __init__(self, ax):
        self.ax = ax
        self.u = np.linspace(0, 2 * np.pi, 15)
        self.v = np.linspace(0, np.pi, 15)
        self.x = np.outer(np.cos(self.u), np.sin(self.v))
        self.y = np.outer(np.sin(self.u), np.sin(self.v))
        self.z = np.outer(np.ones(np.size(self.u)), np.cos(self.v))
        self.sphere = ax.plot_wireframe(self.x, self.y, self.z, color='black')

    def update(self, t):
        distances = self.generate_random_distances(t)
        r = 10 + distances
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                x_new = r[i, j] * np.cos(self.u[i]) * np.sin(self.v[j])
                y_new = r[i, j] * np.sin(self.u[i]) * np.sin(self.v[j])
                z_new = r[i, j] * np.cos(self.v[j])
                self.x[i, j] = x_new
                self.y[i, j] = y_new
                self.z[i, j] = z_new
        self.sphere.remove()
        self.sphere = self.ax.plot_wireframe(self.x, self.y, self.z, color='black')

    def generate_random_distances(self, t, shape=(15, 15)):
        np.random.seed(42)  # Pour obtenir des résultats reproductibles
        noise_scale = 0.3  # Échelle du bruit
        frequency = 0.3 #fréquence de la sinusoïde
        return noise_scale * np.sin(frequency * t) * np.random.normal(0, 1, shape)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')
ax.set_axis_off()

sphere_anim = SphereAnimation(ax)
ani = FuncAnimation(fig, sphere_anim.update, frames=np.arange(0, 360, 1), interval=50)

plt.show()
