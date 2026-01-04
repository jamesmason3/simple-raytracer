# Next update:
# each ray has a set number of light bounces (5)
# make raytrace() recursive to handle bounces
# first check how many bounces are left (function parameter)
# if 0, return ambient light color  
# else, check for intersection
# if intersection, modify color, calculate reflection ray

import numpy as np
import math
import sys

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color
        # self.roughness = roughness

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

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

sphere = Sphere(np.array([-1, -1, 4]), 2, (255, 0, 255)) 
sphere2 = Sphere(np.array([2, 3, 6]), 2, (0, 255, 0)) 

objects = [sphere, sphere2]

pixels = [[(255,255,255) for _ in range(pixel_width)] for _ in range(pixel_height)]

# sphere_color = (1, 0, 1)
ambient_light = 0.3

light_source = np.array([0, 200000, 0])

def raytrace(ray, objects):
    closest_dist = sys.maxsize
    closest_obj = None
    
    for obj in objects:
        vector_to_obj = obj.center - ray.origin
        tca = np.dot(ray.direction, vector_to_obj)

        if tca < 0:
            continue

        d2 = np.dot(vector_to_obj, vector_to_obj) - tca**2
        if d2 > obj.radius * obj.radius:
            continue
        thc = math.sqrt(obj.radius * obj.radius - d2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            continue

        if np.linalg.norm(t0) < closest_dist:
            closest_dist = np.linalg.norm(t0)
            closest_obj = obj
    if closest_obj is not None:
        hit_point = ray.origin + ray.direction * t0
        
        normal = hit_point - closest_obj.center
        normal = normal / np.linalg.norm(normal)
        
        to_light = light_source - hit_point
        to_light = to_light / np.linalg.norm(to_light)
        
        diffuse_intensity = max(np.dot(normal, to_light), 0)
        intensity = ambient_light + (1 - ambient_light) * diffuse_intensity
        diffuse_color = tuple(min(int(c * intensity), 255) for c in closest_obj.color)

        return diffuse_color
    else:
        return (255, 255, 255)


for j in range(pixel_height):
    for i in range(pixel_width):
        u = (i + 0.5) / pixel_width
        v = (j + 0.5) / pixel_height

        x = (u - 0.5) * screen_width
        y = (0.5 - v) * screen_height
        direction = np.array([x, y, focal_length])
        direction = direction / np.linalg.norm(direction)

        # Raytrace
        pixels[j][i] = raytrace(Ray(camera_pos, direction), objects)
        


def create_ppm(filename, width, height, pixels):
    with open(filename, 'w') as f:
        f.write(f'P3 {width} {height} 255\n')
        for j in range(height):
            for i in range(width):
                r, g, b = pixels[j][i]
                f.write(f"{r} {g} {b} ")
            f.write("\n")
        
        

create_ppm('scene.ppm', 256, 256, pixels)