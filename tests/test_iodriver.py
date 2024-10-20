import pygame
import logging
from unittest.mock import patch

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
