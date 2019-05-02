import curses, json
from curses.textpad import Textbox
from .utils import Utility, Data

class UI:
    def __init__(self, screen, lang_file):
        with open(lang_file, 'r') as lfile:  
            self.local = json.load(lfile)
        self.screen = screen
        self.h, self.w = screen.getmaxyx()
        if self.h < 24 or self.w < 80:
            raise EnvironmentError("Minimum required terminal size is 24 rows by 80 cols.")
        self.left_cols = self.w//4
        self.right_cols = self.w//4
        self.link_rows = self.h//4
        
    def draw_borders(self, online=False):
        for y in range(self.h):
            self.screen.addch(y, self.left_cols-1, curses.ACS_VLINE)
            self.screen.addch(y, self.w-self.right_cols, curses.ACS_VLINE)
        for x in range(self.left_cols):
            self.screen.addch(4, x, curses.ACS_HLINE)
        for x in range(self.left_cols, self.w-self.right_cols):
            self.screen.addch(1, x, curses.ACS_HLINE)
        self.screen.addch(1, self.left_cols-1, curses.ACS_LTEE)
        self.screen.addch(4, self.left_cols-1, curses.ACS_RTEE)
        self.screen.addch(1, self.w-self.right_cols, curses.ACS_RTEE)
        if online:
            for x in range(self.w-self.right_cols, self.w):
                self.screen.addch(2, x, curses.ACS_HLINE)
                self.screen.addch(self.h-self.link_rows-1, x, curses.ACS_HLINE)
            self.screen.addch(2, self.w-self.right_cols, curses.ACS_LTEE)
            self.screen.addch(self.h-self.link_rows-1, self.w-self.right_cols, curses.ACS_LTEE)
    
    def draw_captions(self, online=False):
        
        self.screen.addnstr(4, 2, self.local["ui"]["utilities"], self.left_cols-8)
        if online:
            self.screen.addnstr(2, self.w-self.right_cols+2, self.local["ui"]["icons"], self.right_cols-2)
            self.screen.addnstr(self.h-self.link_rows-1, self.w-self.right_cols+2, self.local["ui"]["links"], self.right_cols-2)
        else:
            self.screen.addnstr(0, self.w-self.right_cols+1, self.local["ui"]["storage"], self.right_cols-1)
        self.hardware.addnstr(0, 0, self.local["ui"]["mpcp"], 5)
        self.hardware.addnstr(1, 0, self.local["ui"]["bod"], 5)
        self.hardware.addnstr(2, 0, self.local["ui"]["masking"], 5)
        self.hardware.addnstr(3, 0, self.local["ui"]["memory"], 7)
        self.hardware.addnstr(0, self.left_cols//2, self.local["ui"]["io"], 3)
        self.hardware.addnstr(1, self.left_cols//2, self.local["ui"]["evasion"], 5)
        self.hardware.addnstr(2, self.left_cols//2, self.local["ui"]["sensor"], 5)
        self.status.addnstr(0, 0, self.local["ui"]["pool"], 5)
        self.status.addnstr(0, 10, self.local["ui"]["damage"], 5)
    
    def make_subwindows(self, online=False):
        self.terminal = self.screen.subwin(self.h-2,self.w-self.left_cols-self.right_cols,2,self.left_cols)
        self.hardware = self.screen.subwin(4,self.left_cols-1,0,0)
        self.utilities = self.screen.subwin(self.h-5,self.left_cols-1,5,0)
        self.status = self.screen.subwin(1,self.w-self.left_cols-self.right_cols,0,self.left_cols)
        self.host = None
        self.icons = None
        self.links = None
        self.files = None
        if online:
            self.host = self.screen.subwin(2,self.right_cols-1,0,self.w-self.right_cols+1)
            self.icons = self.screen.subwin(self.h-self.link_rows-4,self.right_cols-1,3,self.w-self.right_cols+1)
            self.links = self.screen.subwin(self.link_rows,self.right_cols-1,self.h-self.link_rows,self.w-self.right_cols+1)
        else:
            self.files = self.screen.subwin(self.h-1,self.right_cols-1,1,self.w-self.right_cols+1)
    
    def show_stats(self, icon):
        self.hardware.addstr(0, 6, str(icon.deck.mpcp).rjust(2))
        self.hardware.addstr(1, 6, str(icon.bod).rjust(2))
        self.hardware.addstr(2, 6, str(icon.masking).rjust(2))
        self.hardware.addstr(0, self.left_cols//2+4, str(icon.io_speed).rjust(4))
        self.hardware.addstr(1, self.left_cols//2+6, str(icon.evasion).rjust(2))
        self.hardware.addstr(2, self.left_cols//2+6, str(icon.sensor).rjust(2))
        self.hardware.addstr(3, self.left_cols//2+2, '/')
        self.hardware.addstr(3, self.left_cols//2-3, str(icon.free_memory()).center(5)) # can't know that yet
        try: self.hardware.addstr(3, self.left_cols//2+3, str(icon.deck.memory).center(5))
        except: pass # Writing bottom-right corner may fail
        if not icon.host:
            self.screen.addnstr(0, self.w-11, str(icon.free_storage()).center(5),5)
            self.screen.addstr(0, self.w-6, '/')
            self.screen.addnstr(0, self.w-5, str(icon.total_storage()).center(5),5)
        self.status.addnstr(0, 6, str(icon.pool).rjust(2),2)
        self.status.addnstr(0, 15, str(icon.damage).rjust(2),2)
        self.status.addnstr(0, self.status.getmaxyx()[1]//2-1, self.local["ui"]["asist_"+icon.mode],4)
        try:
            right = self.status.getmaxyx()[1]
            used = icon.used_actions
            acts = icon.max_actions
            if icon.initiative:
                self.status.addnstr(0, right-15, str(icon.initiative).rjust(2)+':',3)
            self.status.addnstr(0, right-12, str(used),1,[0,curses.A_DIM][icon.simple_action])
            self.status.addnstr(0, right-11, "/%d"%acts,2)
            t = icon.time + used*3//acts
            self.status.addnstr(0, right-8, "%02d:%02d:%02d"%(t//3600,t//60%60,t%60),8)
        except: pass
        
    def show_memory(self, icon):
        self.utilities.clear()
        for n, u in enumerate(icon.in_memory):
            try:
                self.utilities.addnstr(n, 0, u.name+' '+str(u.level), self.right_cols-5)
                self.utilities.addnstr(n, self.right_cols-5, str(u.size).rjust(4), 4)
            except: pass
        
    def show_storage(self, icon):
        self.files.clear()
        for n, u in enumerate(icon.in_storage):
            try:
                self.files.addnstr(n, 0, u.name+' '+str(u.level), self.right_cols-5)
                self.files.addnstr(n, self.right_cols-5, str(u.size).rjust(4), 4)
            except: pass
        
    def show_history(self, icon):
        self.terminal.clear()
        rows, cols = self.terminal.getmaxyx()
        for n,line in enumerate(icon.history[1-rows:]):
            self.terminal.addnstr(n, 0, line, cols)
        
    def show(self, icon):
        self.draw_borders(bool(icon.host))
        self.make_subwindows(bool(icon.host))
        self.draw_captions(bool(icon.host))
        self.show_stats(icon)
        self.show_memory(icon)
        if not icon.host:
            self.show_storage(icon)
        self.show_history(icon)
        self.screen.addstr(self.h-1,self.left_cols,'>')
        self.screen.refresh()
    
    def get_command(self):
        curses.KEY_BACKSPACE = 127 # The constant seems to be wrong.
        cmdwin = self.screen.subwin(1, self.w-self.left_cols-self.right_cols-2, self.h-1, self.left_cols+2)
        cmdbox = Textbox(cmdwin)
        cmdbox.edit()
        cmd = cmdbox.gather()
        cmdwin.clear()
        return cmd
