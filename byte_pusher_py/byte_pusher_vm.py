import numpy as np

class BytePusherVM:
    def __init__(self):
        self.memory = np.zeros(0xFFFFFF, dtype=np.uint8)
    
    def load(self, rom: str):
        pc = 0
        with open(rom, 'rb') as fs:
            while byte := fs.read(1):
                self.memory[pc] = byte[0]
                pc += 1
        
        return self.memory[:pc]
    
    def run(self):
        instruction_counter = 0x10000 # 65536
        pc = self.get_address(2, 3)
        while instruction_counter != 0:
            sourceIndex = self.get_address(pc, 3)
            targetIndex = self.get_address(pc + 3, 3)
            self.memory[targetIndex] = self.memory[sourceIndex]
            pc = self.get_address(pc + 6, 3)
            instruction_counter-=1
    
    def get_address(self, pc: int, length: int) -> int:
        address = 0
        for _ in range(length):
            address = (address << 8) + int(self.memory[pc])
            pc += 1
        return address
                
if __name__ == '__main__':
    vm = BytePusherVM()
    vm.load(r"C:\Users\USUARIO\Downloads\Scrolling Logo.BytePusher")
    