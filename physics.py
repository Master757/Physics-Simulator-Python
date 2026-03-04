import numpy as np

class Particle:
    def __init__(self, x, y, radius=20, parent_id = 1):
        self.pos_now = np.array([x, y], dtype=float)
        self.pos_old = np.array([x, y], dtype=float)
        self.accel = np.array([0.0, 700.0]) 
        self.radius = radius
        self.is_grabbed = False 
        self.friction = 0.99
        self.parent_id = parent_id
    def update(self, dt):
        if self.is_grabbed:
            return 
            
        velocity = (self.pos_now - self.pos_old) * self.friction
        temp_pos = self.pos_now.copy()
        self.pos_now = self.pos_now + velocity + (self.accel * dt * dt)
        self.pos_old = temp_pos

    def constrain(self, width, height, bounce = 0.8):
        bounce = bounce
        fric_l = 0.1
        
        # Bottom
        if self.pos_now[1] > height - self.radius:
            vel_y = self.pos_now[1] - self.pos_old[1]
            self.pos_now[1] = height - self.radius
            self.pos_old[1] = self.pos_now[1] + (vel_y * bounce)
            self.pos_old[0] += (self.pos_now[0] - self.pos_old[0]) * fric_l

        # Top
        if self.pos_now[1] < self.radius:
            vel_y = self.pos_now[1] - self.pos_old[1]
            self.pos_now[1] = self.radius
            self.pos_old[1] = self.pos_now[1] + (vel_y * bounce)
            
        # Right
        if self.pos_now[0] > width - self.radius:
            vel_x = self.pos_now[0] - self.pos_old[0]
            self.pos_now[0] = width - self.radius
            self.pos_old[0] = self.pos_now[0] + (vel_x * bounce)

        # Left
        if self.pos_now[0] < self.radius:
            vel_x = self.pos_now[0] - self.pos_old[0]
            self.pos_now[0] = self.radius
            self.pos_old[0] = self.pos_now[0] + (vel_x * bounce)

        # Preventing infinite vibrations
        if np.linalg.norm(self.pos_now - self.pos_old) < 0.1:
            self.pos_old = self.pos_now.copy()

    def reset(self, x, y):
        self.pos_now = np.array([x, y], dtype=float)
        self.pos_old = np.array([x, y], dtype=float)
        self.is_grabbed = False

def collisions(particles):
    for i in range(len(particles)):
        # Start at i + 1 to avoid self-collision, saves time and space
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]

            diff = p1.pos_now - p2.pos_now
            dist = np.sqrt(np.sum(np.square(diff)))

            d_min = p1.radius + p2.radius
            if dist < d_min:
                if dist == 0:
                    dist = 0.07
                    diff = np.array([dist, 0.0])

                olap = d_min - dist
                normal = diff / dist

                if not p1.is_grabbed:
                    p1.pos_now += normal * (olap * 0.5)
                if not p2.is_grabbed:
                    p2.pos_now -= normal * (olap * 0.5)

class Link:
    def __init__(self, p1, p2, length=None):
        self.p1 = p1
        self.p2 = p2
        # If no length specified, use current distance (break safe)
        diff = p1.pos_now - p2.pos_now
        self.length = length if length else np.sqrt(np.sum(np.square(diff)))

    def resolve(self):
        diff = self.p1.pos_now - self.p2.pos_now
        dist = np.sqrt(np.sum(np.square(diff)))
        
        if dist == 0: return # Prevent division by zero (break safe only- doesnt have any implementations right now)
        
        # Calculate how much to "pull" or "push" to reach perfect length
        error = (self.length - dist) / dist
        percent = error * 0.5
        offset = diff * percent

        if not self.p1.is_grabbed:
            self.p1.pos_now += offset
        if not self.p2.is_grabbed:
            self.p2.pos_now -= offset

def create_filled_box(x, y, size, particles, links, parent_id):
    r = 2 # Small corner radius
    center_r = size / 2 # Big enough to fill the gap
    
    #  Corners
    p1 = Particle(x, y, r, parent_id)
    p2 = Particle(x + size, y, r, parent_id)
    p3 = Particle(x + size, y + size, r, parent_id)
    p4 = Particle(x, y + size, r, parent_id)
    
    # The "Solid" Center
    center_p = Particle(x + size/2, y + size/2, center_r, parent_id)
    
    new_pts = [p1, p2, p3, p4, center_p]
    particles.extend(new_pts)
    
    # Outer Edges (The Frame)
    links.append((parent_id, Link(p1, p2)))
    links.append((parent_id, Link(p2, p3)))
    links.append((parent_id, Link(p3, p4)))
    links.append((parent_id, Link(p4, p1)))
    
    # Connect every corner to the center to keep it perfectly square
    links.append((parent_id, Link(p1, center_p)))   
    links.append((parent_id, Link(p2, center_p)))
    links.append((parent_id, Link(p3, center_p)))
    links.append((parent_id, Link(p4, center_p)))

def create_filled_triangle(x, y, size, particles, links, parent_id):
    r = 2  # Small corner radius
    
    # 1. Define corners (This creates a right-angled triangle)
    p1 = Particle(x, y, r, parent_id)
    p2 = Particle(x + size, y, r, parent_id)
    p3 = Particle(x + size, y + size, r, parent_id)
    
    # Grab positions for the math
    v1, v2, v3 = p1.pos_now, p2.pos_now, p3.pos_now

    # 2. Calculate side lengths (needed for the perfect center and radius)
    side_a = np.linalg.norm(v2 - v3) # Side opposite p1
    side_b = np.linalg.norm(v1 - v3) # Side opposite p2
    side_c = np.linalg.norm(v1 - v2) # Side opposite p3
    
    # This formula weights the coordinates by the lengths of the opposite sides
    total_perimeter = side_a + side_b + side_c
    in_x = (side_a * v1[0] + side_b * v2[0] + side_c * v3[0]) / total_perimeter
    in_y = (side_a * v1[1] + side_b * v2[1] + side_c * v3[1]) / total_perimeter

    # 4. Calculate Inradius
    s = total_perimeter / 2.0
    area = np.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))
    center_r = area / s

    center_p = Particle(in_x, in_y, center_r, parent_id)
    
    new_pts = [p1, p2, p3, center_p]
    particles.extend(new_pts)
    
    # Links
    links.append((parent_id, Link(p1, p2)))
    links.append((parent_id, Link(p2, p3)))
    links.append((parent_id, Link(p3, p1)))
    
    links.append((parent_id, Link(p1, center_p)))   
    links.append((parent_id, Link(p2, center_p)))
    links.append((parent_id, Link(p3, center_p)))