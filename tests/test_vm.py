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