from unittest.mock import MagicMock
import numpy as np
import tempfile
import logging

from byte_pusher_py.byte_pusher_iodriver import BytePusherIODriver
from byte_pusher_py.byte_pusher_vm import BytePusherVM
from byte_pusher_py.log_config import configure_test_logging

configure_test_logging()

def test_load():
    logging.info('Iniciando teste de carregamento da ROM...')
    # Criar um arquivo ROM temporário com dados conhecidos
    with tempfile.NamedTemporaryFile(delete=False) as temp_rom:
        rom_data = bytes([0x01, 0x02, 0x03, 0xFF, 0x00])  # Dados conhecidos
        temp_rom.write(rom_data)
        temp_rom_name = temp_rom.name  # Obter o nome do arquivo temporário
    
    logging.info(f'Rom temporária que deverá ser carregada: {rom_data}')
    # Instanciar o loader
    mock_iodriver = MagicMock(spec=BytePusherIODriver)
    vm = BytePusherVM(iodriver=mock_iodriver)
    
    logging.info('Carregando rom temporária')
    # Carregar a ROM usando o método
    loaded_memory = vm.load(temp_rom_name)
    
    logging.info(f"Primeiros 16 bytes carregados: {bytes(loaded_memory[:16])}")
    
    # Verificar se o conteúdo carregado está correto
    if not np.array_equal(loaded_memory, np.frombuffer(rom_data, dtype=np.uint8)):
        logging.error("ROM carregada incorretamente!\n")
    assert np.array_equal(loaded_memory, np.frombuffer(rom_data, dtype=np.uint8)), "Erro: ROM carregada incorretamente!"
    logging.info('Rom carregada está correto!')

    # Verificar o tamanho correto
    if len(loaded_memory) != len(rom_data):
        logging.error(f"Tamanho incorreto da memória ({len(loaded_memory)} bytes, esperado {len(rom_data)} bytes)\n")
    assert len(loaded_memory) == len(rom_data), f"Erro: Tamanho incorreto da memória ({len(loaded_memory)} bytes, esperado {len(rom_data)} bytes)"
    logging.info('Tamanho final da rom carregada está correto!')
    
    logging.info("Teste de carregamento da rom passou com sucesso!\n")
    
def test_update_pressed_keys():
    logging.info("Iniciando teste de atualização das teclas pressionadas...")

    # Simular o retorno das teclas pressionadas
    mock_iodriver = MagicMock(spec=BytePusherIODriver)
    vm = BytePusherVM(iodriver=mock_iodriver)
    
    # Simular que as teclas K_1 e K_a estão pressionadas
    expected_key_press = 2 + 1024  # K_1 (2) e K_a (1024)
    mock_iodriver.get_key_pressed.return_value = expected_key_press
    
    logging.info(f"Teclas simuladas: K_1 (2) + K_a (1024) = {expected_key_press} ({hex(expected_key_press)})")

    # Chamar o método para atualizar as teclas pressionadas
    logging.info("Chamando update_pressed_keys para atualizar a memória...")
    vm.update_pressed_keys()
    
    # Verificar se os valores corretos foram escritos na memória
    high_byte = expected_key_press >> 8
    low_byte = expected_key_press & 0xFF
    
    logging.info(f"Valores esperados para a memória -> high_byte: {high_byte} ({hex(high_byte)}), low_byte: {low_byte} ({hex(low_byte)})")

    # Verificar memória[0]
    if vm.memory[0] != high_byte:
        logging.error(f"Memória [0] incorreta! Esperado: {high_byte} ({hex(high_byte)}), Obtido: {vm.memory[0]}({hex(vm.memory[0])})\n")
    else:
        logging.info(f"Memória [0] correta: {vm.memory[0]} ({hex(vm.memory[0])})")
    assert vm.memory[0] == high_byte, f"Erro: Memória [0] incorreta! Esperado: {high_byte} ({hex(high_byte)}), Obtido: {vm.memory[0]}"
    
    # Verificar memória[1]
    if vm.memory[1] != low_byte:
        logging.error(f"Memória [1] incorreta! Esperado: {low_byte} ({hex(low_byte)}), Obtido: {vm.memory[1]}({hex(vm.memory[1])})\n")
    else:
        logging.info(f"Memória [1] correta: {vm.memory[1]} ({hex(vm.memory[1])})")
    assert vm.memory[1] == low_byte, f"Erro: Memória [1] incorreta! Esperado: {low_byte} ({hex(low_byte)}), Obtido: {vm.memory[1]}"
    
    logging.info("Teste concluído: Memória atualizada corretamente com as teclas pressionadas!\n")
    
def test_byte_byte_jump():
    logging.info('Iniciando teste do algoritmo byte byte jump...')
    mock_iodriver = MagicMock(spec=BytePusherIODriver)
    vm = BytePusherVM(iodriver=mock_iodriver)

    # Simular a memória com valores conhecidos
    # Exemplo: temos valores nos primeiros 10 bytes da memória
    initial_memory = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 
                                0x05, 0x06, 0x07, 0x08, 0x09], dtype=np.uint8)
    
    # Preencher a memória da VM
    vm.memory = np.zeros(0xFFFFFF, dtype=np.uint8)  # Limpar a memória
    vm.memory[:len(initial_memory)] = initial_memory  # Definir valores iniciais
    
    # Definindo os endereços de origem e destino na memória
    # Simulando as instruções de origem e destino
    # Exemplo: sourceIndex em 0x02 (0x02) = 0x02, e deve ser copiado para memory[0x03] (0x03)
    vm.memory[0:3] = [0x00, 0x00, 0x02]  # sourceIndex = 0x02 (copia de 2)
    vm.memory[3:6] = [0x00, 0x00, 0x03]  # targetIndex = 0x03 (escreve em 3)
    
    # Atualiza pc para apontar para a próxima operação
    vm.memory[6:9] = [0x00, 0x00, 0x04]  # Próximo pc (0x04) para a próxima operação
    
    m_temp = bytes(vm.memory[:10])
    
    logging.info('Objetivo: Copiar o valor de "0x02" e escrever em "0x03"')
    logging.info('Executando algoritmo')
    vm.process_byte_byte_jump()
    
    logging.info(f"Memória antes:  {m_temp}")
    logging.info(f"Memória depois: {bytes(vm.memory[:10])}")
    
    # Esperado: valor de memory[0x03] deve ser igual ao valor de memory[0x02]
    expected_value = initial_memory[2]  # Deverá ser 0x02
    if vm.memory[0x03] != expected_value:
        logging.error(f"Esperado {expected_value}, mas retornou {vm.memory[0x03]}\n")
    assert vm.memory[0x03] == expected_value, f"Erro: Esperado {expected_value}, mas retornou {vm.memory[0x03]}"
    
    logging.info("Teste do algoritmo byte byte jump passou com sucesso!\n")
    
def test_get_address():
    logging.info('Iniciando teste do algoritmo que obtém endereços...')
    mock_iodriver = MagicMock(spec=BytePusherIODriver)
    vm = BytePusherVM(iodriver=mock_iodriver)
    
    # Simular a memória com valores conhecidos (exemplo: [0x12, 0x34, 0x56, 0x78])
    vm.memory = np.array([0x12, 0x34, 0x56, 0x78, 0x90, 0xAB], dtype=np.uint8)
    logging.info(f'Memória simulada: {[hex(b) for b in vm.memory]}')
    
    pc = 0
    length = 2
    logging.info(f'Iniciando com pc em {pc}, leia {length} bytes')
    address = vm.get_address(pc, length)
    
    logging.info('Verificar o valor esperado (0x12 seguido por 0x34 deve formar 0x1234)')
    expected_address = 0x1234
    if address != expected_address:
        logging.error(f"Esperado {hex(expected_address)}, mas retornou {hex(address)}\n")
    assert address == expected_address, f"Erro: Esperado {hex(expected_address)}, mas retornou {hex(address)}"
    logging.info(f'Endereço esperado: {hex(expected_address)}, endereço obtido: {hex(address)}')
    
    pc = 2
    length = 3
    logging.info(f'Iniciando com pc em {pc}, leia {length} bytes')
    address = vm.get_address(pc, length)
    
    logging.info('Verificar o valor esperado (0x56 seguido por 0x78 e 0x90 deve formar 0x567890)')
    expected_address = 0x567890
    if address != expected_address:
        logging.error(f"Esperado {hex(expected_address)}, mas retornou {hex(address)}\n")
    assert address == expected_address, f"Erro: Esperado {hex(expected_address)}, mas retornou {hex(address)}"
    logging.info(f'Endereço esperado: {hex(expected_address)}, endereço obtido: {hex(address)}')
    
    logging.info("Teste do método de obter endereçoes passou com sucesso!\n")
    
def test_copy():
    logging.info('Iniciando teste do método copy...')

    mock_iodriver = MagicMock(spec=BytePusherIODriver)
    vm = BytePusherVM(iodriver=mock_iodriver)
    vm.memory = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09], dtype=np.uint8)

    logging.info(f'Memória inicial: {vm.memory}')

    start = 2
    length = 5
    logging.info(f'Testar a cópia com parâmetros válidos -> start: {start}, length: {length}')
    copied_memory = vm.copy(start, length)

    expected_memory = np.array([0x02, 0x03, 0x04, 0x05, 0x06], dtype=np.uint8)
    logging.info(f'Memória copiada (esperado): {expected_memory}')
    logging.info(f'Memória copiada (obtido):   {copied_memory}')

    # Verificar se a cópia está correta
    if not np.array_equal(copied_memory, expected_memory):
        logging.error("Cópia da memória está incorreta!\n")
    assert np.array_equal(copied_memory, expected_memory), "Erro: Cópia da memória está incorreta!"
    logging.info('Cópia da memória está correta!')

    start = 7
    length = 5
    logging.info(f'Testar a cópia com limites fora do range -> start: {start}, length: {length}')
    copied_memory = vm.copy(start, length)

    expected_memory = np.array([0x07, 0x08, 0x09], dtype=np.uint8)
    logging.info(f'Memória copiada (esperado): {expected_memory}')
    logging.info(f'Memória copiada (obtido):   {copied_memory}')

    # Verificar se a cópia está correta
    if not np.array_equal(copied_memory, expected_memory):
        logging.error("Cópia da memória está incorreta ao ultrapassar limites!\n")
    assert np.array_equal(copied_memory, expected_memory), "Erro: Cópia da memória está incorreta ao ultrapassar limites!"
    logging.info('Cópia da memória com limites está correta!')

    start = 10  # Fora dos limites
    length = 5
    logging.info(f'Testar a cópia com start fora do range -> start: {start}, length: {length}')
    copied_memory = vm.copy(start, length)

    expected_memory = np.array([], dtype=np.uint8)  # Esperado nada
    logging.info(f'Memória copiada (esperado): {expected_memory}')
    logging.info(f'Memória copiada (obtido):   {copied_memory}')

    # Verificar se a cópia está correta
    if not np.array_equal(copied_memory, expected_memory):
        logging.error("Cópia da memória não deveria retornar dados!\n")
    assert np.array_equal(copied_memory, expected_memory), "Erro: Cópia da memória não deveria retornar dados!"
    logging.info('Cópia da memória quando start está fora do range está correta!')

    logging.info("Teste do método copy passou com sucesso!\n")