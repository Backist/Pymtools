from colorama import Fore, Back, Style
from random import choice


def cFormatter(
    string: str, 
    color: str, 
    style: Style = None, 
    background: Back = None, 
    random: bool = False, 
    iter_colors: list[Fore] = []
) -> str:
    """
    Formateador de texto en terminal.
    Valido con cadenas de texto, listas de texto y docstrings.
    """
    
    #init(autoreset= autoreset)


    # c = vars(Fore)
    # s = vars(Style)
    # b = vars(Back)

    # if not color in c.keys():
    #     print(f"{Fore.RED}| {color} | no es un color valido.")
    # elif not style in s.keys():
    #      print(f"{Fore.RED}| {style} | no es un estilo valido.")
    # elif not background in b.keys():
    #     print(f"{Fore.RED}| {background} | no es un subrayador valido.")

    # else:

    #     if iter_colors:
    #         if len(iter_colors) == 0 or [x for x in iter_colors if x not in c.keys()]:
    #             return TypeError(cFormatter("No se ha definido una lista de colores con los que iterar o algun color no es valido", color= Fore.RED))
    #         else: 
    #             letters = []
    #             for chars in string:
    #                 letters.append(f"{choice(iter_colors)}{chars}{Fore.RESET}")
    #             return "".join(letters)

    #     elif random:
    #         rcolor = choice(c.values())
    #         rstyle = choice(s.values())
    #         rback = choice(b.values())
    #         return f"{rcolor}{rstyle}{rback}{string}{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"

    #     elif color:
    #         if background:
    #             return f"{c[color]}{b[background]}{string}{Fore.RESET}{Back.RESET}"
    #         elif style:
    #             return f"{c[color]}{s[style]}{string}{Fore.RESET}{Style.RESET_ALL}"
    #         else:
    #             return f"{c[color]}{string}{Fore.RESET}"


    c = [Fore.BLACK, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA, Fore.WHITE, Fore.LIGHTCYAN_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTBLACK_EX, Fore.LIGHTYELLOW_EX]
    s = [Style.DIM, Style.NORMAL, Style.BRIGHT]
    b = [Back.BLACK, Back.RED, Back.BLUE, Back.CYAN, Back.GREEN, Back.MAGENTA, Back.YELLOW, Back.WHITE, Back.LIGHTBLACK_EX, Back.LIGHTBLUE_EX, 
    Back.LIGHTCYAN_EX, Back.LIGHTGREEN_EX, Back.LIGHTMAGENTA_EX, Back.LIGHTYELLOW_EX, Back.LIGHTWHITE_EX]

    if (color is not None and not color in c) or (style is not None and not style in s) or (background is not None and not background in b):
        return ValueError(cFormatter(f"Color o estilo o fondo no valido", color= Fore.RED))

    else:

        if iter_colors:
            if len(iter_colors) == 0 or [x for x in iter_colors if x not in c]:
                return TypeError(cFormatter("No se ha definido una lista de colores con los que iterar o algun color no es valido", color= Fore.RED))
            else: 
                letters = []
                for chars in string:
                    letters.append(f"{choice(iter_colors)}{chars}{Fore.RESET}")
                return "".join(letters)

        elif random:
            rcolor = choice(c)
            rstyle = choice(s)
            rback = choice(b)
            return f"{rcolor}{rstyle}{rback}{string}{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"

        elif color:
            if background:
                return f"{color}{background}{string}{Fore.RESET}{Back.RESET}"
            elif style:
                return f"{color}{style}{string}{Fore.RESET}{Style.RESET_ALL}"
            else:
                return f"{color}{string}{Fore.RESET}"