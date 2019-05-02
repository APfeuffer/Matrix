import json
from .deck import Deck
from .utils import Utility

class Decker:
    def __init__(self, **kwargs):
        if kwargs: self.from_dict(kwargs)

    def from_dict(self, tree):
        self.abilities = tree.get("abilities",{})
        self.cyberware = tree.get("cyberware",[])
        self.gear = tree.get("gear",[])
        self.skills = tree.get("skills",{})
        self.knowledge = tree.get("knowledge",{})
        self.base_tnmod = tree.get("base_tnmod",0) # from edges and flaws
        self.stun_damage = tree.get("stun_damage",0)
        self.phys_damage = tree.get("phys_damage",0)
        self.utilities = [Utility(u["type"],u["level"],u.get("options",{})) for u in tree.get("utilities",[])]
        self.deck = tree.get("deck", "CMT Portal")
        if isinstance(self.deck, str): self.deck=Deck().from_file(f"decks/{self.deck}.json")
        elif isinstance(self.deck, dict): self.deck=Deck().from_dict(self.deck)
        persona = tree.get("persona")
        if isinstance(persona, list) and 4==len(persona): self.deck.persona = persona
        elif isinstance(persona, dict): self.deck.persona = [persona.get("Bod",0),
                                                             persona.get("Evasion",0),
                                                             persona.get("Masking",0),
                                                             persona.get("Sensor",0)]
        return self
    
    def from_file(self, path):
        with open(path, 'r') as jfile:  
            return self.from_dict(json.load(jfile))

    @property
    def body(self):
        return self.abilities.get("body",3) # There is no 'ware that increases body for decking purposes
    
    @property
    def intelligence(self):
        intl = self.abilities.get("intelligence",3)
        for ware in self.cyberware:
            if ware.get("type","")=="Cerebral Booster":
                intl+=ware.get("level",1)
        return intl
    
    @property
    def willpower(self):
        return self.abilities.get("willpower",3) # There is no 'ware that increases willpower, period
    
    def damage_mod(self):
        mod = 0
        if self.stun_damage>=10: mod+=4 # Praise the almighty stim patch!
        elif self.stun_damage>=6: mod+=3
        elif self.stun_damage>=3: mod+=2
        elif self.stun_damage>=1: mod+=1
        if self.phys_damage>=10: mod+=4
        elif self.phys_damage>=6: mod+=3
        elif self.phys_damage>=3: mod+=2
        elif self.phys_damage>=1: mod+=1
        return mod
    
    def tn_mod(self):
        return self.base_tnmod + self.damage_mod()
    
    def initiative(self):
        ri=self.deck.response
        return 1+ri, self.intelligence+2*ri-self.damage_mod()
        
    def hacking_pool(self):
        pool = (self.intelligence + self.deck.mpcp)//3
        for ware in self.cyberware:
            wtype=ware.get("type","")
            if wtype=="Encephalon" or wtype=="Math SPU":
                pool+=ware.get("level",1)
        return pool
        
    def task_pool(self):
        for ware in self.cyberware:
            if ware.get("type","")=="Encephalon":
                return ware.get("level",1)
        return 0
    
    def skill(self, skill, specs=[]):
        level = self.skills.get(skill,0)
        for spec in specs:
            level = max(level, self.skills.get(spec,0))
        return level
    
    def knowledge(self, skill, specs=[]):
        level = self.knowledge.get(skill,0)
        for spec in specs:
            level = max(level, self.knowledge.get(spec,0))
        return level
