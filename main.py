import pygame
import numpy as np
import physics
from physics import Particle
from presentation import Render
import pyautogui # type: ignore

def main():
    #defaults
    WIDTH, HEIGHT = pyautogui.size()
    FPS = 60
    bounce = 0.8
    DT = 1.0 / FPS
    prev_gravity = 700.0
    current_gravity = 700.0
    
    renderer = Render(WIDTH, HEIGHT)
    clock = pygame.time.Clock()
    
    particles = []
    links = []
    
    square_ids = []
    triangle_ids = []
    id_s = 10
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                
                # Spawning
                if event.key == pygame.K_1: # Spawn Ball
                    particles.append(Particle(WIDTH//2, HEIGHT//2, 20))
                
                if event.key == pygame.K_2: # Spawn Filled Box
                    x, y = WIDTH//2, HEIGHT//2
                    physics.create_filled_box(x, y, 80, particles, links, id_s)
                    square_ids.append(id_s)
                    id_s += 1
                
                if event.key == pygame.K_3:
                    x, y = WIDTH//2, HEIGHT//2
                    physics.create_filled_triangle(x, y, 80, particles, links, id_s)
                    triangle_ids.append(id_s)
                    id_s += 1

                if event.key == pygame.K_o:
                    bounce += 0.1

                if event.key == pygame.K_p:
                    bounce -= 0.1
                
                # Controls
                if event.key == pygame.K_r: # Reset
                    particles.clear()
                    links.clear()
                
                # Gravity Controls
                if event.key == pygame.K_UP:
                    prev_gravity = current_gravity
                    current_gravity += 100.0
                if event.key == pygame.K_DOWN:
                    prev_gravity = current_gravity
                    current_gravity -= 100.0
                if event.key == pygame.K_z:
                    if current_gravity == 0.0:
                        current_gravity = prev_gravity
                    else:
                        prev_gravity =current_gravity
                        current_gravity = 0.0

            # Mouse Interactions
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)
                
                if event.button == 1: # Left Click: Grab
                    for p in particles:
                        if renderer.is_mouse_on_ball(mouse_pos, p):
                            p.is_grabbed = True
                            break 
                
                if event.button == 3: # Right Click: Delete
                    for i in range(len(particles) - 1, -1, -1):
                        if renderer.is_mouse_on_ball(mouse_pos, particles[i]):
                            # If we delete a particle, we must clear links to avoid crashes
                            del_id = particles[i].parent_id
                            if del_id == 1: #simple deletion for a simple sphere
                                particles.pop(i)
                                break

                            if del_id in square_ids or del_id in triangle_ids:
                                for i in range(len(particles) -1, -1, -1):
                                    if particles[i].parent_id == del_id:
                                        particles.pop(i)
                                    
                                for i in range(len(links) -1, -1, -1):
                                    if links[i][0] == del_id:
                                        links.pop(i)
                                        
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for p in particles:
                        p.is_grabbed = False

        keys = pygame.key.get_pressed()
        for p in particles:
            if p.is_grabbed:
                if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
                    p.radius += 1
                if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
                    p.radius = max(5, p.radius - 1)

        for p in particles:
            p.accel[1] = current_gravity # Sync gravity
            if p.is_grabbed:
                mouse_now = np.array(pygame.mouse.get_pos(), dtype=float)
                mouse_move = (mouse_now - p.pos_now) * 0.15
                p.pos_old = p.pos_now.copy()
                p.pos_now += mouse_move
            else:
                p.update(DT)

        # Solving links and collisions multiple times makes the boxes rigid
        for _ in range(10):
            for parent_id, link in links:
                link.resolve()
            physics.collisions(particles)
            for p in particles:
                p.constrain(WIDTH, HEIGHT, bounce)

        renderer.clear()
        
        # Draw Links
        for parent_id, link in links:
            pygame.draw.line(renderer.screen, (100, 100, 100), 
                             link.p1.pos_now, link.p2.pos_now, 2)
            
        # Draw Particles
        for p in particles:
            renderer.draw_particle(p)
        
        renderer.draw_stats(current_gravity, len(particles), bounce)
        renderer.update_display()
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
