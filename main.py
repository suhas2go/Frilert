from systray import SysTrayIcon
from headBrowse import bye


if __name__ == '__main__':
    import itertools, glob
    favicon = itertools.cycle(glob.glob(r"icons\favicon.ico"))
    hover_text = "Frilert"   
    SysTrayIcon(next(favicon), hover_text, on_quit=bye, default_menu_index=1)