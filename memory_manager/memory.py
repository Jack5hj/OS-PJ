import pickle
import os
from collections import OrderedDict

class MemoryManager:
    def __init__(self, capacity=3, swap_enabled=True, log_callback=None,policy="fifo"):
        self.capacity = capacity
        self.memory = OrderedDict()
        self.swap_enabled = swap_enabled
        self.log_callback = log_callback 
        self.policy = policy 
        self.current= None

    def log(self, msg):
        print(msg)
        if self.log_callback:
            self.log_callback(msg)

    def load_segment(self, name, loader):
        self.current = name
        if name in self.memory:
            self.memory.move_to_end(name)
            self.log(f"✅ Accessed (in-memory): {name}")
        else:
            if len(self.memory) >= self.capacity:
                if self.swap_enabled:
                    self.swap_out()
                else:
                    self.log("⚠️ Memory full, no swap!")
            self.memory[name] = loader(name)
            self.log(f"✅ Loaded to memory: {name}")
            self.log(f"🧠 Memory state: {list(self.memory.keys())}")

    def swap_out(self):
        if self.policy == "fifo":
            old_key, old_data = self.memory.popitem(last=False)
        elif self.policy == "smart":
            for key in self.memory:
                 if key != self.current:  
                    old_key = key
                    break
            old_data = self.memory.pop(old_key)
            with open(f"swap_{old_key}.seg", "wb") as f:
                    pickle.dump(old_data, f)
            self.log(f"📤 Swap Out: {old_key}")
            self.log(f"🧠 Memory state after swap: {list(self.memory.keys())}")

    def swap_in(self, name):
        with open(f'swap_{name}.seg', 'rb') as f:
            data = pickle.load(f)
        self.memory[name] = data
        os.remove(f'swap_{name}.seg')
        self.log(f"📥 Swap In: {name}")
