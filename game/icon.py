from .deck import Deck
from .char import Decker
from .utils import *
from random import randrange

class Icon:
    def __init__(self, decker, max_io = None):
        self.decker = decker
        self.deck = decker.deck
        self.damage = 0
        self.pool = decker.hacking_pool()
        self.storage = self.total_storage()
        if max_io: self.io_speed = min(self.deck.io_speed,max_io)
        else: self.io_speed = self.deck.io_speed
        self.in_storage = decker.utilities
        self.in_memory = []
        self.bod = decker.deck.bod
        self.evasion = decker.deck.evasion
        self.masking = decker.deck.masking
        self.sensor = decker.deck.sensor
        self.host = None
        self.mode = ["cold", "hot"][self.deck.hot_asist]
        self.new_round(True)
        self.time = 0 # seconds
        self.history=[]
        self.active = True
    
    def total_storage(self):
        storage = self.deck.storage
        for ware in self.decker.cyberware:
            if ware.get("type").find("Memory")>=0:
                storage+=ware.get("amount",0)
        for item in self.decker.gear:
            if item.get("type").find("Memory")>=0:
                storage+=ware.get("amount",0)
        return storage

    def used_storage(self):
        return total_size(self.in_storage)
    def used_memory(self):
        return total_size(self.in_memory)
    def free_storage(self):
        return self.storage-self.used_storage()
    def free_memory(self):
        return self.deck.memory-self.used_memory()
    
    def new_round(self, combat=False):
        self.pool = self.decker.hacking_pool()
        ini = self.decker.initiative()
        self.simple_action = False
        self.free_action = False
        self.used_actions = 0
        try: self.time+=3
        except: pass
        if combat:
            self.initiative = ini[1]
            for roll in range(ini[0]):
                self.initiative+=randrange(1,6)
            self.max_actions = 1+self.initiative//10
        else:
            self.initiative = None
            self.max_actions = ini[0]+(ini[1]-1)//10
    
    def resolve_command(self, cmd):
        if not cmd.strip(): return
        self.history.append('> '+cmd)
        toks = cmd.lower().split(' ')
        syscmds = {
            "load": self.load,
            "unload": self.unload,
            "shutdown": self.shutdown
            }
        #try:
        if toks[0] in syscmds: syscmds[toks[0]](*toks)
        else: self.history.append(f"Command not found: {toks[0].capitalize()}")
        #except:
        #    self.history.append(f"Invalid Arguments to {toks[0].capitalize()}")
            
    def load(self, *args):
        for u in self.in_storage:
            mlvl = u.match(args[1:])
            if mlvl:
                loaded = [um for um in self.in_memory if um.copyof==u]
                if loaded and not "oneshot" in u.options:
                    self.history.append("Only One-Shots can be loaded twice.")
                    return
                elif mlvl>self.deck.mpcp:
                    self.history.append("Unable to run at Rating %d"%mlvl)
                    return
                elif u.size>self.free_memory():
                    self.history.append("Out of Memory.")
                    return
                else:
                    self.in_memory.append(u.copy())
                    self.in_memory[-1].level = mlvl
                    self.history.append("Loaded %s %d"%(u.name,mlvl))
                    return
        self.history.append("Could not find matching Utility.")
        
    def unload(self, *args):
        for i,u in enumerate(self.in_memory):
            if u.match(args[1:]):
                head = self.in_memory[:i] or []
                tail = self.in_memory[i+1:] or []
                self.in_memory = head+tail
                self.history.append("Unloaded %s %d"%(u.name,u.level))
                return
        self.history.append("Could not find matching Utility.")

    def shutdown(self, *args):
        if self.host:
            self.history.append("Shutdown while jacked in. Roll for dump shock.")
            self.active=False
        else:
            self.active=False
            
