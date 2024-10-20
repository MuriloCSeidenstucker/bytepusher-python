import pygame

class BytePusherIODriver:
    def __init__(self):
        pygame.init()

    def get_key_pressed(self):
        key = 0
        
        # Captura o estado das teclas
        pressed_keys = pygame.key.get_pressed()
        
        # Verifica quais teclas estão pressionadas
        if pressed_keys[pygame.K_0]: key += 1
        if pressed_keys[pygame.K_1]: key += 2
        if pressed_keys[pygame.K_2]: key += 4
        if pressed_keys[pygame.K_3]: key += 8
        if pressed_keys[pygame.K_4]: key += 16
        if pressed_keys[pygame.K_5]: key += 32
        if pressed_keys[pygame.K_6]: key += 64
        if pressed_keys[pygame.K_7]: key += 128
        if pressed_keys[pygame.K_8]: key += 256
        if pressed_keys[pygame.K_9]: key += 512
        if pressed_keys[pygame.K_a]: key += 1024
        if pressed_keys[pygame.K_b]: key += 2048
        if pressed_keys[pygame.K_c]: key += 4096
        if pressed_keys[pygame.K_d]: key += 8192
        if pressed_keys[pygame.K_e]: key += 16384
        if pressed_keys[pygame.K_f]: key += 32768
        
        return key

if __name__ == "__main__":
    iodriver = BytePusherIODriver()
    
    # Configuração da janela do Pygame
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Key Press Example")

    # Loop principal do Pygame
    running = True
    last_key_pressed = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key_press = iodriver.get_key_pressed()
        if key_press != 0:
            if key_press == last_key_pressed:
                pass
            else:
                print(f"Key Pressed Value: {key_press}")
                last_key_pressed = key_press

        # Atualizar a tela (opcional)
        screen.fill((0, 0, 0))  # Limpa a tela
        pygame.display.flip()    # Atualiza a tela

    pygame.quit()
