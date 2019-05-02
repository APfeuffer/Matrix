from curses import wrapper
from game.ui import UI
from game.char import Decker
from game.icon import Icon

def main(screen):
    global c
    ui = UI(screen,"local/english.json")
    decker=Decker().from_file("chars/combat_decker.json")
    icon=Icon(decker)
    while icon.active:
        ui.show(icon)
        cmd = ui.get_command()
        icon.resolve_command(cmd)

if __name__ == "__main__":
    wrapper(main)
