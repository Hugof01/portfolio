import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import textwrap

class SphereAnimation:
    def __init__(self, ax, text_ax, rotation_speed=1, color_speed=1):
        self.ax = ax
        self.text_ax = text_ax
        self.u = np.linspace(0, 2 * np.pi, 15)
        self.v = np.linspace(0, np.pi, 15)
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
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#%^&*()'
        self.alphabet_markers = self.create_alphabet_markers()
        self.character_list = []
        self.text_annotation = self.text_ax.text(0, 1, '', transform=self.text_ax.transAxes, color='white', fontsize=10, ha='left', va='top')

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

        characters = self.get_characters_on_vertices()
        self.character_list.extend(characters)

        max_length = 1000
        if len(self.character_list) > max_length:
            self.character_list = self.character_list[-max_length:]

        self.update_vertex_characters()

        # Mise à jour du texte d'annotation avec le contenu de character_list
        wrapped_text = '\n'.join(textwrap.wrap(', '.join(self.character_list[:670]), width=80))
        self.text_annotation.set_text('Characters:\n' + wrapped_text)

    def generate_random_distances(self, t, shape=(15, 15)):
        np.random.seed(42)
        noise_scale = 0.3
        frequency = 0.3
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

    def get_characters_on_vertices(self):
        characters = []
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                characters.append(self.get_alphabet_character(self.x[i, j], self.y[i, j], self.z[i, j]))
        return characters

    def update_vertex_characters(self):
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                self.alphabet_markers[i * len(self.x) + j].set_text(self.character_list[i * len(self.x) + j])

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(121, projection='3d')  # Sous-plot pour la sphère
ax.set_facecolor('black')
ax.set_axis_off()

text_ax = fig.add_subplot(122)  # Sous-plot pour la liste
text_ax.set_facecolor('black')
text_ax.set_xlim(0, 1)
text_ax.set_ylim(0, 1)
text_ax.set_axis_off()

sphere_anim = SphereAnimation(ax, text_ax, color_speed=0.5)
ani = FuncAnimation(fig, sphere_anim.update, frames=np.arange(0, 360, 1), interval=50)

fig.patch.set_facecolor('black')  # Changer la couleur de fond de la figure

pause_ax = fig.add_axes([0.4, 0.05, 0.1, 0.05])  # Création de l'axe pour le bouton de pause
pause_button = plt.Button(pause_ax, 'Pause', color='darkred', hovercolor='red')


copy_ax = fig.add_axes([0.5, 0.05, 0.1, 0.05])  # Création de l'axe pour le bouton de copie
copy_button = plt.Button(copy_ax, 'Copy', color='darkred', hovercolor='red')

plt.show()
