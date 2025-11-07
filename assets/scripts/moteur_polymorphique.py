import pygame
import math
import random

# Initialisation de Pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
background_color=(36,97,132)

# Définition des dimensions de la fenêtre
largeur = 800
hauteur = 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Réseau de Connexion en 3D")

# Classe pour représenter un point en 3D
class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def rotate_x(self, angle):
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotate_y(self, angle):
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotate_z(self, angle):
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, largeur, hauteur, fov, distance):
        z_offset = 0.0001  # Ajout d'une petite valeur à la coordonnée z
        factor = fov / (distance + self.z + z_offset)
        x = self.x * factor + largeur / 2
        y = -self.y * factor + hauteur / 2
        return Point3D(x, y, 0)

# Générer des points aléatoires en 3D sur la surface d'une sphère
def generate_sphere_points(num_points, radius):
    points = []
    for _ in range(num_points):
        u = random.uniform(0, 1)
        v = random.uniform(0, 1)
        theta = 2 * math.pi * u
        phi = math.acos(2 * v - 1)
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        points.append(Point3D(x, y, z))
    return points

# Générer des arêtes entre les points aléatoires
def generate_edges(points):
    aretes = []
    for i in range(len(points)):
        # Choisir deux points aléatoires différents
        j, k = random.sample(range(len(points)), 2)
        while j == i or k == i:
            j, k = random.sample(range(len(points)), 2)
        # Ajouter les arêtes entre le point i et les points j et k
        aretes.append((points[i], points[j]))
        aretes.append((points[i], points[k]))
    return aretes

# Générer des points sur une sphère
rayon_sphere = 3
points = generate_sphere_points(104, rayon_sphere)

# Générer des arêtes une seule fois
aretes = generate_edges(points)

# Boucle principale du jeu
en_cours = True
horloge = pygame.time.Clock()

while en_cours:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # Effacer l'écran
    fenetre.fill(background_color)

    # Mouvement aléatoire des points avec inertie
    for point in points:
        # Générer une accélération aléatoire pour chaque composante
        ax = random.uniform(-0.01, 0.01)
        ay = random.uniform(-0.01, 0.01)
        az = random.uniform(-0.01, 0.01)
        # Appliquer l'accélération à la vitesse
        point.vx += ax
        point.vy += ay
        point.vz += az
        # Limiter la vitesse maximale
        max_speed = 0.5
        point.vx = max(-max_speed, min(point.vx, max_speed))
        point.vy = max(-max_speed, min(point.vy, max_speed))
        point.vz = max(-max_speed, min(point.vz, max_speed))
        # Appliquer la vitesse à la position
        point.x += point.vx
        point.y += point.vy
        point.z += point.vz
        # Ramener le point à l'intérieur de la sphère si nécessaire
        distance_from_center = math.sqrt(point.x ** 2 + point.y ** 2 + point.z ** 2)
        if distance_from_center > rayon_sphere:
            # Normaliser les coordonnées pour ramener le point à la surface de la sphère
            point.x *= rayon_sphere / distance_from_center
            point.y *= rayon_sphere / distance_from_center
            point.z *= rayon_sphere / distance_from_center

    # Projection et affichage des arêtes
    for arete in aretes:
        p1 = arete[0].project(largeur, hauteur, 256, 4)
        p2 = arete[1].project(largeur, hauteur, 256, 4)
        pygame.draw.aaline(fenetre, BLANC, (p1.x, p1.y), (p2.x, p2.y))

    # Actualiser l'affichage
    pygame.display.flip()

    # Limiter le taux de rafraîchissement de l'écran
    horloge.tick(30)

# Quitter Pygame
pygame.quit()
