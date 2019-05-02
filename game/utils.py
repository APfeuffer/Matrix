
options = {
    "A": {"adaptive", "bugridden", "crashguard", "dinab", "noise", "oneshot", "optimization", "sensitive", "sneak", "squeeze"},
    "B": {"adaptive", "bugridden", "crashguard", "optimization", "squeeze"},
    "C": {"adaptive", "area", "bugridden", "chaser", "crashguard", "dinab", "limit", "noise", "oneshot", "optimization", "penetration", "selective", "stealth", "targeting"},
    "D": {"adaptive", "bugridden","crashguard", "oneshot", "optimization","selective", "targeting"},
    "E": {"adaptive", "area", "bugridden", "crashguard", "dinab", "oneshot", "optimization", "selective", "targeting"},
    "F": {"adaptive", "bugridden", "crashguard", "dinab", "oneshot", "optimization", "selective", "targeting"},
    "G": {"adaptive", "bugridden", "crashguard", "dinab", "oneshot", "optimization", "stealth", "targeting"},
    "H": {"adaptive", "bugridden", "crashguard", "optimization"},
    "J": {"adaptive", "bugridden", "crashguard", "oneshot", "optimization"},
    "K": {"adaptive", "bugridden", "crashguard", "dinab", "optimization"},
    "L": {"adaptive", "bugridden", "crashguard", "dinab", "oneshot", "optimization"}
}
utils = {
    "Analyze": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Browse": {"multiplier": 1, "type": "Operational", "options": options["A"]},
    "Camo": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Commlink": {"multiplier": 1, "type": "Operational", "options": options["A"]},
    "Crash": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Deception": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Decrypt": {"multiplier": 1, "type": "Operational", "options": options["A"]},
    "Defuse": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Encrypt": {"multiplier": 1, "type": "Operational", "options": options["A"]},
    "Evaluate": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Mirrors": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Purge": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Read/Write": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Redecorate": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Relocate": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Scanner": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Sniffer": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Snooper": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Spoof": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Swerve": {"multiplier": 3, "type": "Operational", "options": options["A"]},
    "Triangulation": {"multiplier": 2, "type": "Operational", "options": options["A"]},
    "Validate": {"multiplier": 4, "type": "Operational", "options": options["A"]},
    "BattleTac": {"multiplier": 5, "type": "Link", "options": options["B"]},
    "Cellular": {"multiplier": 1, "type": "Link", "options": options["B"]},
    "Maser": {"multiplier": 1, "type": "Link", "options": options["B"]},
    "Microwave": {"multiplier": 1, "type": "Link", "options": options["B"]},
    "Radio": {"multiplier": 1, "type": "Link", "options": options["B"]},
    "Satellite": {"multiplier": 2, "type": "Link", "options": options["B"]},
    "Compressor": {"multiplier": 2, "type": "Special", "options": options["B"]},
    "Guardian": {"multiplier": 2, "type": "Special", "options": options["B"]},
    "Remote Control": {"multiplier": 3, "type": "Special", "options": options["B"]},
    "Sleaze": {"multiplier": 3, "type": "Special", "options": options["B"]},
    "Track": {"multiplier": 8, "type": "Special", "options": options["B"]},
    "Attack-L": {"multiplier": 2, "type": "Offensive", "options": options["C"]},
    "Attack-M": {"multiplier": 3, "type": "Offensive", "options": options["C"]},
    "Attack-S": {"multiplier": 4, "type": "Offensive", "options": options["C"]},
    "Attack-D": {"multiplier": 5, "type": "Offensive", "options": options["C"]},
    "Black Hammer": {"multiplier": 20, "type": "Offensive", "options": options["D"]},
    "Erosion": {"multiplier": 3, "type": "Offensive", "options": options["E"]},
    "Hog": {"multiplier": 3, "type": "Offensive", "options": options["F"]},
    "Killjoy": {"multiplier": 10, "type": "Offensive", "options": options["D"]},
    "Slow": {"multiplier": 4, "type": "Offensive", "options": options["E"]},
    "Steamroller": {"multiplier": 3, "type": "Offensive", "options": options["G"]},
    "Armor": {"multiplier": 3, "type": "Defensive", "options": options["H"]},
    "Cloak": {"multiplier": 3, "type": "Defensive", "options": options["J"]},
    "Lock-On": {"multiplier": 3, "type": "Defensive", "options": options["J"]},
    "Medic": {"multiplier": 4, "type": "Defensive", "options": options["K"]},
    "Restore": {"multiplier": 3, "type": "Defensive", "options": options["L"]},
    "Shield": {"multiplier": 4, "type": "Defensive", "options": options["H"]}
}
def regularize(name):
    return name.replace('/','').replace('-','').replace('_','').replace(' ','').lower()
pretty = {regularize(key):key for key in utils.keys()}
aliases = {"read": "readwrite", "write": "readwrite"}
def alias(name):
    return aliases.get(name,name)

class Utility:
    def __init__(self, name, level, options={}):
        self.regname = regularize(name)
        self.level = level
        self.options = {regularize(o):v for o,v in options.items()}
        self.copyof = None
        
    def copy(self):
        cp = Utility(self.regname, self.level, self.options)
        cp.copyof = self
        return cp
    
    def match(self, toks):
        lvl = self.level
        while toks and not toks[-1]: toks=toks[:-1]
        if len(toks)>0 and alias(regularize(toks[0]))==self.regname: i = 1
        elif len(toks)>1 and alias(regularize(toks[0]+toks[1]))==self.regname: i = 2
        else: return 0
        if len(toks)>i:
            lvl = int(toks[i])
            if lvl==self.level: i+=1
            elif "adaptive" in self.options and lvl<self.level: i+=1
            else: return 0
        for t in toks[i:]:
            if '-'==t[0]:
                t = t[1:]
                if regularize(t) in options: return 0
            else:
                ts = t.split('=')
                if not regularize(ts[0]) in options: return 0
                elif len(ts)>1 and str(options[regularize(ts[0])])!=ts[1]: return 0
        return lvl
    
    @property
    def name(self):
        return pretty[self.regname]
    
    @property
    def size(self): # ignore options for now
        if self.copyof: return self.copyof.size
        else: return utils[self.name]["multiplier"]*self.level*self.level

class Data:
    def __init__(self, name, size):
        self.name = name
        self.regname = regularize(name)
        self.size = size
        self.copyof = None

def total_size(files):
    return sum([f.size for f in files])
