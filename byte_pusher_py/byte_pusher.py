import pygame

from byte_pusher_py.byte_pusher_iodriver import BytePusherIODriver
from byte_pusher_py.byte_pusher_vm import BytePusherVM

class BytePusher:
    def __init__(self):
        pygame.init()
        
        # Define a resolução da tela (256x256 pixels, por exemplo)
        self.screen = pygame.display.set_mode((256, 256))

        pygame.display.set_caption("BytePusherPython")
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        
        self.iodriver = BytePusherIODriver(self.screen)
        self.vm = BytePusherVM(self.iodriver)

    def load_rom(self, rom: str):
        self.vm.load(rom)  # Carrega o ROM na VM

    def update(self):
        # Loop principal do Pygame
        while self.running:
            self.handle_events()
            
            self.vm.run()

            # Calcula os FPS
            fps = self.clock.get_fps()
            
            # Exibe FPS, CPU e GPU na tela
            self.display_fps(fps)

            # Limita o FPS para 60 quadros por segundo
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def draw(self):
        pass
    
    def display_fps(self, fps):
        fps_text = self.font.render(f'FPS: {fps:.2f}', True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        pygame.display.update()

    def cleanup(self):
        pygame.quit()

if __name__ == "__main__":
    byte_pusher = BytePusher()
    byte_pusher.load_rom(r"C:\Users\mseid\Downloads\nyan.bp")
    byte_pusher.update()
    byte_pusher.cleanup()
