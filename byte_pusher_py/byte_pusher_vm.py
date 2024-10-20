import numpy as np

from byte_pusher_py.byte_pusher_iodriver import BytePusherIODriver

class BytePusherVM:
    def __init__(self, iodriver: BytePusherIODriver):
        self.memory = np.zeros(0xFFFFFF, dtype=np.uint8)
        self.iodriver = iodriver
    
    def load(self, rom: str):
        pc = 0
        with open(rom, 'rb') as fs:
            while byte := fs.read(1):
                self.memory[pc] = byte[0]
                pc += 1
        
        return self.memory[:pc]
    
    def run(self):
        self.update_pressed_keys()
        self.process_byte_byte_jump()
    
    def get_address(self, pc: int, length: int) -> int:
        address = 0
        for _ in range(length):
            address = (address << 8) + int(self.memory[pc])
            pc += 1
        return address
    
    def update_pressed_keys(self):
        keys_pressed = self.iodriver.get_key_pressed()
        self.memory[0] = (keys_pressed & 0xFF00) >> 8
        self.memory[1] = keys_pressed & 0xFF
    
    def process_byte_byte_jump(self):
        instruction_counter = 0x10000 # 65536
        pc = self.get_address(2, 3)
        while instruction_counter != 0:
            sourceIndex = self.get_address(pc, 3)
            targetIndex = self.get_address(pc + 3, 3)
            self.memory[targetIndex] = self.memory[sourceIndex]
            pc = self.get_address(pc + 6, 3)
            instruction_counter-=1
                
if __name__ == '__main__':
    vm = BytePusherVM()
    vm.load(r"C:\Users\USUARIO\Downloads\Scrolling Logo.BytePusher")
    