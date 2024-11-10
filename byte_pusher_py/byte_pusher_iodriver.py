import numpy as np
import pygame
import logging

from byte_pusher_py.log_config import configure_test_logging

configure_test_logging()

class BytePusherIODriver:
    def __init__(self, screen):
        # Cria o buffer RGB (256x256 com 3 canais para RGB)
        self.rgbuffer = np.zeros((256, 256, 3), dtype=np.uint8)
        self.screen = screen

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

    def render_display_frame(self, data):
        self.rgbuffer.fill(0)  # Limpa o buffer RGB
        
        for i, c in enumerate(data):
            if c < 0 or c > 255:
                continue  # Ignora valores fora do intervalo

            # Cálculo dos componentes de cor
            if c < 216:
                red = (c // 36) % 6
                green = (c // 6) % 6
                blue = c % 6
            else:
                # Valores de 216 a 255 são pretos
                red, green, blue = 0, 0, 0

            # Multiplicando por 51 para obter a intensidade correta (0 a 255)
            red_color = red * 51
            green_color = green * 51
            blue_color = blue * 51

            # Determinando a posição x, y
            x = i % 256  # Posição x
            y = i // 256  # Posição y

            # Renderiza a cor no buffer
            self.rgbuffer[x, y] = [red_color, green_color, blue_color]

        # Atualiza a tela com o buffer RGB usando surfarray
        pygame.surfarray.blit_array(self.screen, self.rgbuffer)
        pygame.display.flip()