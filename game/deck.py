import json

class Deck:
    def __init__(self, **kwargs):
        if kwargs: self.from_dict(kwargs)
        
    def estimate_cost(self):
        return int((self.mpcp**3.36)*7)*50
    
    def default_persona(self):
        if self.hot_asist:
            persona = [self.mpcp*3//4]*4
            diff = 3*self.mpcp-sum(persona)
            if diff>=1: persona[3]+=1
            if diff>=2: persona[0]+=1
            if diff>=3: persona[1]+=1
        else:
            persona = [self.mpcp*3//2, 0, 0, self.mpcp*3//2+self.mpcp%2]
        return persona
    
    def from_dict(self, tree):
        self.name = tree.get("name","Custom")
        self.mpcp = tree.get("mpcp",1)
        self.hardening = tree.get("hardening",0)
        self.memory = tree.get("memory",50)
        self.storage = tree.get("storage",100)
        self.io_speed = tree.get("io_speed",50)
        self.response = tree.get("response",0)
        self.hot_asist = tree.get("hot_asist",self.mpcp>2)
        self.iccm = tree.get("iccm",False)
        self.reality_filter = tree.get("reality_filter",False)
        self.cost = tree.get("cost",self.estimate_cost())
        try:
            p = tree["persona"]
            self.persona = [p.get("Bod",0), p.get("Evasion",0),
                            p.get("Masking",0), p.get("Sensor",0)]
        except: self.persona = self.default_persona()
        return self
    
    def from_file(self, path):
        with open(path, 'r') as jfile:  
            return self.from_dict(json.load(jfile))
        
    @property
    def bod(self):
        try: return self.persona[0]
        except: return 0
    
    @property
    def evasion(self):
        try: return self.persona[1]
        except: return 0
    
    @property
    def masking(self):
        try: return self.persona[2]
        except: return 0
    
    @property
    def sensor(self):
        try: return self.persona[3]
        except: return 0
