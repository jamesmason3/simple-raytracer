import numpy as np
import math

class Sphere:
  def __init__(self, center, radius):
    self.center = center
    self.radius = radius
    # self.color = color
    # self.roughness = roughness

#pixels
pixel_width = 256
pixel_height = 256
# aspect_ratio = width / height

camera_pos = np.array([0, 0, 0])
focal_length = 1.0

#screen is a square
#theta (ideally pass in)
camera_fov = 90
screen_width = 2 * focal_length * math.tan(math.radians(camera_fov) / 2)
screen_height = screen_width

sphere = Sphere(np.array([0, 0, 4]), 2) 
sphere2 = Sphere(np.array([1, 1, 5]), 3) 

pixels = [[(255,255,255) for _ in range(pixel_width)] for _ in range(pixel_height)]


for j in range(pixel_height):
    for i in range(pixel_width):
        u = (i + 0.5) / pixel_width
        v = (j + 0.5) / pixel_height

        x = (u - 0.5) * screen_width
        y = (0.5 - v) * screen_height
        direction = np.array([x, y, focal_length])
        direction = direction / np.linalg.norm(direction)

        # blue sphere calculation
        L = sphere2.center - camera_pos
        tca = np.dot(direction, L)
 
        # Camera is inside sphere
        if tca < 0:
            continue

        d = math.sqrt(np.dot(L, L) - tca**2)
        if d < sphere2.radius:
            thc = math.sqrt(sphere2.radius**2 - d**2)
            t0 = tca - thc
            t1 = tca + thc
            pixels[j][i] = (0, 0, 255)

        # red sphere calculation
        L = sphere.center - camera_pos
        tca = np.dot(direction, L)
 
        # Camera is inside sphere
        if tca < 0:
            continue

        d = math.sqrt(np.dot(L, L) - tca**2)
        if d < sphere.radius:
            thc = math.sqrt(sphere.radius**2 - d**2)
            t0 = tca - thc
            t1 = tca + thc
            pixels[j][i] = (255, 0, 0)


def create_ppm(filename, width, height, pixels):
    with open(filename, 'w') as f:
        f.write(f'P3 {width} {height} 255\n')
        for j in range(height):
            for i in range(width):
                r, g, b = pixels[j][i]
                f.write(f"{r} {g} {b} ")
            f.write("\n")
        
        

create_ppm('scene.ppm', 256, 256, pixels)