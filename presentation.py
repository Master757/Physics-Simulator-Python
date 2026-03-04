import numpy as np
import pygame

class Render:
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Verlet Physics-Sandbox Simulator")
        self.font = pygame.font.SysFont("Arial", 24)
        
    # MOVE THIS OUTSIDE OF __init__
    def draw_stats(self, gravity_value, particle_count, bounce_text):
        grav_text = f"Gravity: {gravity_value:.0f}"
        count_text = f"Particles: {particle_count}"
        bounce_text = f"Bounce Factor: {bounce_text:.1f}"

        grav_surf = self.font.render(grav_text, True, (255, 255, 255))
        count_surf = self.font.render(count_text, True, (255, 255, 255))
        bounce_surf = self.font.render(bounce_text, True, (255,255,255))
        
        self.screen.blit(grav_surf, (20, 5))
        self.screen.blit(count_surf, (20, 35))
        self.screen.blit(bounce_surf, (20, 65))

    def clear(self):
        self.screen.fill((30,30,30))
    
    def draw_particle(self, particle, colour=(0, 255, 150)):
        pygame.draw.circle(self.screen, colour, particle.pos_now.astype(int), particle.radius)

    def is_mouse_on_ball(self, mouse_pos, particle):
        diff = mouse_pos - particle.pos_now
        dist = np.sqrt(np.sum(np.square(diff)))
        return dist < particle.radius
    
    def update_display(self):
        pygame.display.flip()