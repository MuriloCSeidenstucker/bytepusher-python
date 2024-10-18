import numpy as np

class BytePusherVM:
    
    def load(self, rom: str):
        memory = np.zeros(0xFFFFFF, dtype=np.uint8)
        pc = 0
        with open(rom, 'rb') as fs:
            while byte := fs.read(1):
                memory[pc] = byte[0]
                pc += 1
        
        return memory[:pc]
                
if __name__ == '__main__':
    vm = BytePusherVM()
    vm.load(r"C:\Users\USUARIO\Downloads\Scrolling Logo.BytePusher")