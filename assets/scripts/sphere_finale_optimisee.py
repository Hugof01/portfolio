import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class SphereAnimation:
    def __init__(self, ax, rotation_speed=1, color_speed=1):
        self.ax = ax
        self.u = np.linspace(0, 2 * np.pi, 10)  # Diminution du nombre de points pour la sphère
        self.v = np.linspace(0, np.pi, 10)      # Diminution du nombre de points pour la sphère
        self.x = np.outer(np.cos(self.u), np.sin(self.v))
        self.y = np.outer(np.sin(self.u), np.sin(self.v))
        self.z = np.outer(np.ones(np.size(self.u)), np.cos(self.v))
        self.sphere = ax.plot_wireframe(self.x, self.y, self.z, color='white', linewidth=2)
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.rotation_speed = rotation_speed
        self.color_speed = color_speed
        self.glowing_colors = self.generate_glowing_colors()
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()'
        self.alphabet_markers = self.create_alphabet_markers()

    def update(self, t):
        distances = self.generate_random_distances(t)
        r = 10 + distances
        max_distance = np.max(r)
        r /= max_distance

        self.angle_x += 0.00001 * self.rotation_speed
        self.angle_y += 0.00002 * self.rotation_speed
        self.angle_z += 0.00005 * self.rotation_speed

        rotation_matrix_x = np.array([[1, 0, 0],
                                      [0, np.cos(self.angle_x), -np.sin(self.angle_x)],
                                      [0, np.sin(self.angle_x), np.cos(self.angle_x)]])
        
        rotation_matrix_y = np.array([[np.cos(self.angle_y), 0, np.sin(self.angle_y)],
                                      [0, 1, 0],
                                      [-np.sin(self.angle_y), 0, np.cos(self.angle_y)]])
        
        rotation_matrix_z = np.array([[np.cos(self.angle_z), -np.sin(self.angle_z), 0],
                                      [np.sin(self.angle_z), np.cos(self.angle_z), 0],
                                      [0, 0, 1]])

        rotated_xyz = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, np.array([self.x.flatten(), self.y.flatten(), self.z.flatten()]))))
        self.x = np.reshape(rotated_xyz[0], self.x.shape)
        self.y = np.reshape(rotated_xyz[1], self.y.shape)
        self.z = np.reshape(rotated_xyz[2], self.z.shape)

        self.x *= r
        self.y *= r
        self.z *= r

        self.sphere.remove()
        self.sphere = self.ax.plot_wireframe(self.x, self.y, self.z, color='white', linewidth=1, alpha=0.8)

        for marker in self.alphabet_markers:
            marker.remove()
        self.alphabet_markers = self.create_alphabet_markers()

        self.update_glowing_colors(t)

    def generate_random_distances(self, t, shape=(10, 10)):
        np.random.seed(42)
        noise_scale = 0.3
        frequency = 0.1
        return noise_scale * np.sin(frequency * t) * np.random.normal(0, 1, shape)
    
    def generate_glowing_colors(self):
        cmap = plt.cm.Reds
        glowing_colors = cmap(np.linspace(0.2, 1, len(self.x)))
        return glowing_colors
    
    def update_glowing_colors(self, t):
        color_shift = int(t % len(self.x) * self.color_speed)
        self.glowing_colors = np.roll(self.glowing_colors, -color_shift, axis=0)
        self.sphere.set_edgecolors(self.glowing_colors)
    
    def create_alphabet_markers(self):
        markers = []
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                x = self.x[i, j]
                y = self.y[i, j]
                z = self.z[i, j]
                marker = self.ax.text(x, y, z, self.get_alphabet_character(x, y, z), color='white', fontsize=8, ha='center', va='center')
                markers.append(marker)
        return markers
    
    def get_alphabet_character(self, x, y, z):
        index = hash((x, y, z))
        return self.alphabet[index % len(self.alphabet)].upper()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.set_axis_off()

sphere_anim = SphereAnimation(ax, color_speed=0.5)
ani = FuncAnimation(fig, sphere_anim.update, frames=np.arange(0, 360, 1), interval=20)  # Augmentation de la fréquence d'images

plt.show()
