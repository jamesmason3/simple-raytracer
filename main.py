# create objects as light sources

import numpy as np
import math
import sys

class Sphere:
    def __init__(self, center, radius, color, roughness, shininess):
        self.center = center
        self.radius = radius
        self.color = color
        self.roughness = roughness
        self.shininess = shininess
        self.is_light = False

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

#pixels
pixel_width = 512
pixel_height = 512
# aspect_ratio = width / height
camera_pos = np.array([0, 0, 0])
focal_length = 1.0

#screen is a square
#theta (ideally pass in)
camera_fov = 90
screen_width = 2 * focal_length * math.tan(math.radians(camera_fov) / 2)
screen_height = screen_width


objects = [
    Sphere(np.array([0, -1, 2]), 1.0, (200, 200, 200), 0.75, 100), # mirror sphere
    Sphere(np.array([2, 0, 2]), 1.0, (0, 0, 255), 0.1, 40),
    Sphere(np.array([-2, 0, 2]), 1.0, (0, 255, 0), 0.01, 25), # green sphere
]

light_source = np.array([0, 5, 0])

pixels = [[(255,255,255) for _ in range(pixel_width)] for _ in range(pixel_height)]

ambient_light = 0.2
shininess = 50

def raytrace(ray, objects, bounces_left):
    if bounces_left == 0:
        return (0, 0, 0)
    
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
        
        if np.dot(ray.direction, normal) > 0:
            normal = -normal
    
        to_light = light_source - hit_point
        to_light = to_light / np.linalg.norm(to_light)
        
        # Specular 
        view_dir = -ray.direction
        half_vec = to_light + view_dir
        half_vec = half_vec / np.linalg.norm(half_vec)
        
        specular = max(np.dot(normal, half_vec), 0) ** closest_obj.shininess
        specular_color = int(255 * specular)
        
        diffuse_intensity = max(np.dot(normal, to_light), 0)
        intensity = ambient_light + (1 - ambient_light) * diffuse_intensity
        diffuse_color = tuple(min(int(c * intensity + specular_color), 255) for c in closest_obj.color)
        
        # Calculate reflection ray
        reflect_dir = ray.direction - 2 * np.dot(ray.direction, normal) * normal
        reflect_dir = reflect_dir / np.linalg.norm(reflect_dir)
        reflect_ray = Ray(hit_point + normal * 1e-5, reflect_dir)

        # Recursive call
        reflected_color = raytrace(reflect_ray, objects, bounces_left - 1)

        # Calculate final color with roughness
        final_color = tuple(
            min(int(
                (1 - closest_obj.roughness) * d +
                closest_obj.roughness * r
            ), 255)
            for d, r in zip(diffuse_color, reflected_color)
)
        
        return final_color
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
        pixels[j][i] = raytrace(Ray(camera_pos, direction), objects, 5)
        


def create_ppm(filename, width, height, pixels):
    with open(filename, 'w') as f:
        f.write(f'P3 {width} {height} 255\n')
        for j in range(height):
            for i in range(width):
                r, g, b = pixels[j][i]
                f.write(f"{r} {g} {b} ")
            f.write("\n")
        
        

create_ppm('scene.ppm', 512, 512, pixels)