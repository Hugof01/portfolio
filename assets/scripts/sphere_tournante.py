import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class SphereAnimation:
    def __init__(self, ax, rotation_speed=1):
        self.ax = ax
        self.u = np.linspace(0, 2 * np.pi, 15)
        self.v = np.linspace(0, np.pi, 15)
        self.x = np.outer(np.cos(self.u), np.sin(self.v))
        self.y = np.outer(np.sin(self.u), np.sin(self.v))
        self.z = np.outer(np.ones(np.size(self.u)), np.cos(self.v))
        self.sphere = ax.plot_wireframe(self.x, self.y, self.z, color='black')
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.rotation_speed = rotation_speed

    def update(self, t):
        distances = self.generate_random_distances(t)
        r = 10 + distances
        
        # Rotation autour de l'axe x
        rotation_matrix_x = np.array([[1, 0, 0],
                                      [0, np.cos(self.angle_x), -np.sin(self.angle_x)],
                                      [0, np.sin(self.angle_x), np.cos(self.angle_x)]])
        
        # Rotation autour de l'axe y
        rotation_matrix_y = np.array([[np.cos(self.angle_y), 0, np.sin(self.angle_y)],
                                      [0, 1, 0],
                                      [-np.sin(self.angle_y), 0, np.cos(self.angle_y)]])
        
        # Rotation autour de l'axe z
        rotation_matrix_z = np.array([[np.cos(self.angle_z), -np.sin(self.angle_z), 0],
                                      [np.sin(self.angle_z), np.cos(self.angle_z), 0],
                                      [0, 0, 1]])

        # Application des rotations
        rotated_xyz = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, np.array([self.x.flatten(), self.y.flatten(), self.z.flatten()]))))
        
        # Reconstruction des coordonnées x, y, z
        self.x = np.reshape(rotated_xyz[0], self.x.shape)
        self.y = np.reshape(rotated_xyz[1], self.y.shape)
        self.z = np.reshape(rotated_xyz[2], self.z.shape)
        
        self.sphere.remove()
        self.sphere = self.ax.plot_wireframe(self.x, self.y, self.z, color='black')
        
        # Augmentation des angles de rotation en fonction de la vitesse de rotation
        self.angle_x += 0.00001 * self.rotation_speed
        self.angle_y += 0.00002 * self.rotation_speed
        self.angle_z += 0.00005 * self.rotation_speed

    def generate_random_distances(self, t, shape=(15, 15)):
        np.random.seed(42)  # Pour obtenir des résultats reproductibles
        noise_scale = 0.3  # Échelle du bruit
        frequency = 0.3  # Fréquence de la sinusoïde
        return noise_scale * np.sin(frequency * t) * np.random.normal(0, 1, shape)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')
ax.set_axis_off()

# Vous pouvez ajuster la vitesse de rotation en changeant la valeur de rotation_speed
sphere_anim = SphereAnimation(ax, rotation_speed=1)
ani = FuncAnimation(fig, sphere_anim.update, frames=np.arange(0, 360, 1), interval=50)

plt.show()
