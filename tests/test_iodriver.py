import pygame
import logging
from unittest.mock import MagicMock, patch

from byte_pusher_py.byte_pusher_iodriver import BytePusherIODriver
from byte_pusher_py.log_config import configure_test_logging

configure_test_logging()

class TestBytePusherIODriver:

    @patch('pygame.key.get_pressed')
    def test_get_key_press(self, mock_get_pressed):
        logging.info('Iniciando teste: test_get_key_press...')
        logging.info('Simulando as teclas pressionadas: "K_1(2)" e "K_2(4)"')
        mock_get_pressed.return_value = [False] * 256  # Cria uma lista de 256 False
        mock_get_pressed.return_value[pygame.K_1] = True  # Simula K_1 pressionada
        mock_get_pressed.return_value[pygame.K_2] = True  # Simula K_2 pressionada

        driver = BytePusherIODriver()
        key_press = driver.get_key_pressed()

        logging.info('Valor esperado é: K_1(2) + K_2(4) -> "6"')
        expected_value = 2 + 4  # K_1 (2) + K_2 (4)
        if key_press != expected_value:
            logging.error(f"Esperado {expected_value}, mas retornou {key_press}\n")
        assert key_press == expected_value
        logging.info(f"Esperado {expected_value}, retornou {key_press}")
        
        logging.info('Teste finalizado com sucesso: test_get_key_press\n')
        
    @patch('pygame.Surface')
    def test_render_display_frame(self, mock_surface):
        logging.info('Iniciando teste: test_render_display_frame...')
        
        # Mocka uma instância de Surface
        mock_surface_instance = MagicMock()
        mock_surface.return_value = mock_surface_instance

        # Instancia a classe
        driver = BytePusherIODriver()

        # Cria um conjunto de dados para teste (256x256 = 65536 bytes)
        test_data = bytearray([i % 256 for i in range(65536)])
        logging.info('Dados de teste gerados com 65536 bytes')

        # Chama o método a ser testado
        driver.render_display_frame(test_data)
        logging.info('Método render_display_frame executado')

        # Verifica se a textura foi criada corretamente
        mock_surface.assert_called_once_with((256, 256))
        logging.info('A textura de 256x256 foi criada corretamente')

        # Contar quantos pixels devem ser pretos (valores acima de 215)
        black_pixels = sum(1 for c in test_data if c > 215)
        colored_pixels = 65536 - black_pixels  # Restante dos pixels que têm cor
        logging.info(f'Pixels pretos: {black_pixels} | Pixels coloridos: {colored_pixels}')

        # Verifica se o método set_at foi chamado o número correto de vezes
        if mock_surface_instance.set_at.call_count != 65536:
            logging.error(f"Esperado 65536 chamadas ao método set_at, mas retornou {mock_surface_instance.set_at.call_count}\n")
        assert mock_surface_instance.set_at.call_count == 65536
        logging.info(f'O método set_at foi chamado 65536 vezes conforme esperado')

        # Testa se os pixels pretos foram configurados corretamente
        expected_black = pygame.Color(0, 0, 0)
        mock_surface_instance.set_at.assert_any_call((0, 0), expected_black)
        logging.info(f'Pixels pretos foram configurados corretamente')

        logging.info('Teste finalizado com sucesso: test_render_display_frame\n')
