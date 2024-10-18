import numpy as np
import tempfile

from byte_pusher_py.byte_pusher_vm import BytePusherVM

def test_load():
    # Criar um arquivo ROM temporário com dados conhecidos
    with tempfile.NamedTemporaryFile(delete=False) as temp_rom:
        rom_data = bytes([0x01, 0x02, 0x03, 0xFF, 0x00])  # Dados conhecidos
        temp_rom.write(rom_data)
        temp_rom_name = temp_rom.name  # Obter o nome do arquivo temporário
    
    # Instanciar o loader
    loader = BytePusherVM()
    
    # Carregar a ROM usando o método
    loaded_memory = loader.load(temp_rom_name)
    
    print("Primeiros 16 bytes carregados:", loaded_memory[:16])           
    
    # Verificar se o conteúdo carregado está correto
    assert np.array_equal(loaded_memory, np.frombuffer(rom_data, dtype=np.uint8)), "Erro: ROM carregada incorretamente!"

    # Verificar o tamanho correto
    assert len(loaded_memory) == len(rom_data), f"Erro: Tamanho incorreto da memória ({len(loaded_memory)} bytes, esperado {len(rom_data)} bytes)"
    
    print("Teste passou com sucesso!")
    
def test_get_address():
    vm = BytePusherVM()
    
    # Simular a memória com valores conhecidos (exemplo: [0x12, 0x34, 0x56, 0x78])
    vm.memory = np.array([0x12, 0x34, 0x56, 0x78, 0x90, 0xAB], dtype=np.uint8)
    
    pc = 0
    length = 2
    address = vm.get_address(pc, length)
    
    # Verificar o valor esperado (0x12 seguido por 0x34 deve formar 0x1234)
    expected_address = 0x1234
    assert address == expected_address, f"Erro: Esperado {hex(expected_address)}, mas retornou {hex(address)}"
    
    pc = 2
    length = 3
    address = vm.get_address(pc, length)
    
    # Verificar o valor esperado (0x56 seguido por 0x78 e 0x90 deve formar 0x567890)
    expected_address = 0x567890
    assert address == expected_address, f"Erro: Esperado {hex(expected_address)}, mas retornou {hex(address)}"
    
    print("Todos os testes passaram!")