import pygame
import threading
from auth import is_reptor_easter_egg, register_user, login_user, promote_user
from wiki import fetch_scp_article
from lore_db import get_lore_topic

pygame.init()
WIDTH, HEIGHT = 960, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SCiPNET // FOUNDATION TERMINAL OS")

font = pygame.font.Font(None, 26)
title_font = pygame.font.Font(None, 38)

# Colors
BG = (10, 22, 15)
GREEN = (0, 255, 100)
GOLD = (255, 200, 50)
RED = (255, 60, 60)
GRAY = (140, 165, 150)

# Draw an initial frame immediately to avoid a Wayland black screen.
screen.fill(BG)
screen.blit(title_font.render("SCiPNET BOOTING...", True, GREEN), (50, 70))
pygame.display.flip()

# States: MENU, LOGIN, REGISTER, TERMINAL
state = "MENU"
current_user = None
lang = "en"

input_buffer = ""
status_msg = ""
login_step = 0
login_name = ""
login_pass = ""

reg_step = 0
reg_prompts = (
    "1/7 Personnel Name (required):",
    "2/7 Password (required):",
    "3/7 Security Clearance [0-5] (required):",
    "4/7 Personnel Class (e.g. Researcher / Security / Agent):",
    "5/7 Assigned Site (e.g. Site-19):",
    "6/7 [OPTIONAL] MTF Unit (press Enter to skip):",
    "7/7 [OPTIONAL] Committee (e.g. Ethics Committee, press Enter to skip):",
)
reg_answers = []

terminal_lines = []
scroll_y = 0
is_loading = False


def get_theme_color():
    if current_user and current_user.get("is_o5"):
        return GOLD
    return GREEN


def start_wiki_fetch(query):
    global terminal_lines, scroll_y, is_loading
    is_loading = True
    scroll_y = 0
    terminal_lines = [f"> CONNECTING TO SCiPNET DATABASE ({lang.upper()})..."]

    def worker():
        global terminal_lines, is_loading
        result = fetch_scp_article(query, current_user, lang)
        terminal_lines = result
        is_loading = False

    threading.Thread(target=worker, daemon=True).start()


def handle_terminal_command(cmd):
    global terminal_lines, scroll_y, state, current_user, lang
    parts = cmd.strip().split(" ", 1)
    base = parts.pop(0).lower()
    arg = parts.pop(0).strip() if parts else ""
    scroll_y = 0

    if base == "help":
        terminal_lines = [
            "=== AVAILABLE SCiPNET COMMANDS ===",
            "  scp <number>         -> Loads an SCP file (e.g. 'scp 173' or 'scp 001')",
            "  info <topic>         -> Foundation handbook (mtf, sites, ranks, clearance,",
            "                          classes, medications, scenarios)",
            "  lang <de/en>         -> Changes the SCP Wiki language (current: " + lang.upper() + ")",
            "  profile              -> Shows your personnel file, MTF, and committee",
            "  clear                -> Clears the terminal",
            "  logout               -> Logs out and returns to the main menu",
        ]
        if current_user.get("clearance", 0) >= 5:
            terminal_lines.append("  promote <user> <0-5> -> Promotes or demotes a personnel account")

    elif base == "scp" and arg:
        start_wiki_fetch(arg)

    elif base == "info":
        terminal_lines = get_lore_topic(arg)

    elif base == "promote":
        args = arg.split()
        if len(args) != 2:
            terminal_lines = ["USAGE: promote <username> <level 0-5>"]
        else:
            target_user, new_lvl = args
            ok, msg = promote_user(current_user, target_user, new_lvl)
            terminal_lines = [msg]

    elif base == "lang" and arg.lower() in ("de", "en"):
        lang = arg.lower()
        terminal_lines = [f"SCP WIKI LANGUAGE SET TO: {lang.upper()}"]

    elif base == "profile":
        u = current_user
        terminal_lines = [
            "=========================================",
            "          FOUNDATION PERSONNEL FILE       ",
            "=========================================",
            f"  NAME:        {u.get('name')} ({u.get('title', 'Standard')})",
            f"  CLEARANCE:   LEVEL {u.get('clearance')}",
            f"  PERSONNEL:   {u.get('personnel')}",
            f"  SITE:        {u.get('site')}",
            f"  MTF UNIT:    {u.get('mtf')}",
            f"  COMMITTEE:   {u.get('committee')}",
            "=========================================",
        ]

    elif base == "clear":
        terminal_lines = []

    elif base == "logout":
        current_user = None
        state = "MENU"

    else:
        terminal_lines = [f"[UNKNOWN COMMAND: '{cmd}'] Type 'help' to list available commands."]


running = True
while running:
    screen.fill(BG)
    theme = get_theme_color()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL and state == "TERMINAL":
            scroll_y = min(0, scroll_y + event.y * 28)

        elif event.type == pygame.KEYDOWN:
            if state == "EASTER_EGG":
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    state = "MENU"
                    input_buffer = ""
                    status_msg = ""

            elif event.key == pygame.K_ESCAPE and state in ("LOGIN", "REGISTER"):
                state = "MENU"
                input_buffer = ""
                status_msg = ""

            elif event.key == pygame.K_BACKSPACE:
                input_buffer = input_buffer[:-1]

            elif event.key == pygame.K_RETURN:
                val = input_buffer
                input_buffer = ""

                if state == "MENU":
                    if val.strip() == "1":
                        state = "LOGIN"
                        login_step = 0
                        login_name = ""
                        login_pass = ""
                        status_msg = ""
                    elif val.strip() == "2":
                        state = "REGISTER"
                        reg_step = 0
                        reg_answers = []
                        status_msg = ""
                    else:
                        status_msg = "PLEASE ENTER '1' TO LOGIN OR '2' TO REGISTER."

                elif state == "LOGIN":
                    if login_step == 0:
                        login_name = val.strip()
                        login_step = 1
                    else:
                        login_pass = val.strip()
                        if is_reptor_easter_egg(login_name, login_pass):
                            current_user = None
                            state = "EASTER_EGG"
                            login_step = 0
                            login_name = ""
                            login_pass = ""
                        else:
                            ok, res = login_user(login_name, login_pass)
                            if ok:
                                current_user = res
                                state = "TERMINAL"
                                welcome = "OVERSEER COUNCIL VERIFIED" if res.get("is_o5") else "ACCESS GRANTED"
                                terminal_lines = [
                                    f"*** {welcome} // WELCOME {res.get('name')} ***",
                                    f"SITE: {res.get('site')} | CLEARANCE: LEVEL {res.get('clearance')}",
                                    "Type 'help' for commands, 'info' for the handbook, or 'scp 173' to read an SCP file.",
                                ]
                            else:
                                status_msg = res
                                login_step = 0

                elif state == "REGISTER":
                    reg_answers.append(val)
                    reg_step += 1
                    if reg_step >= len(reg_prompts):
                        ok, res = register_user(*reg_answers)
                        if ok:
                            status_msg = "REGISTRATION SUCCESSFUL! PRESS '1' TO LOG IN."
                            state = "MENU"
                        else:
                            status_msg = f"ERROR: {res}"
                            reg_step = 0
                            reg_answers = []

                elif state == "TERMINAL" and val.strip() and not is_loading:
                    handle_terminal_command(val)

            else:
                if event.unicode and event.unicode.isprintable():
                    input_buffer += event.unicode

    if state == "MENU":
        screen.blit(title_font.render("SCP FOUNDATION // SCiPNET TERMINAL", True, GREEN), (50, 70))
        screen.blit(font.render("SECURE. CONTAIN. PROTECT.", True, GRAY), (50, 110))
        screen.blit(font.render("1) LOGIN (Personnel or O5 authorization)", True, GREEN), (50, 190))
        screen.blit(font.render("2) REGISTER NEW PERSONNEL", True, GREEN), (50, 230))
        if status_msg:
            screen.blit(font.render(status_msg, True, RED), (50, 300))
        screen.blit(font.render(f"SELECTION > {input_buffer}_", True, GREEN), (50, 360))

    elif state == "LOGIN":
        screen.blit(title_font.render("SCiPNET // SYSTEM LOGIN (ESC = BACK)", True, GREEN), (50, 70))
        prompt = "Enter username (e.g. name or O5-1..O5-12):" if login_step == 0 else "Enter password:"
        display_in = input_buffer if login_step == 0 else "*" * len(input_buffer)
        screen.blit(font.render(prompt, True, GREEN), (50, 160))
        screen.blit(font.render(f"> {display_in}_", True, GREEN), (50, 200))
        if status_msg:
            screen.blit(font.render(status_msg, True, RED), (50, 260))

    elif state == "EASTER_EGG":
        title = title_font.render("SCiPNET // ACCESS DENIED", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
        for index, message in enumerate((
            "IP Localisation: On going",
            "IP Localisation: Successfull",
            "MTF Unit underway",
        )):
            text = font.render(message, True, RED)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 220 + index * 48)))
        lore = (
            "Reptor is an Enemy of the Foundation, this Enterprise destroyed two "
            "Tornado Jets in Site 20-DE in Switzerland with an Anomaly, that was "
            "build by Reptor, more Informations on the German Channel SCP-Stiftung "
            "the link: https://www.youtube.com/watch?v=8cWtIHLbLRo"
        )
        lines = []
        line = ""
        for word in lore.split():
            candidate = f"{line} {word}".strip()
            if font.size(candidate)[0] > WIDTH - 80 and line:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        for index, message in enumerate(lines):
            text = font.render(message, True, GRAY)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 360 + index * 30)))
        note = font.render("SIMULATION ONLY - NO LOCATION DATA IS COLLECTED", True, GRAY)
        screen.blit(note, note.get_rect(center=(WIDTH // 2, 540)))
        prompt = font.render("Press Enter or Esc to return", True, GREEN)
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 585)))

    elif state == "REGISTER":
        screen.blit(title_font.render("CREATE PERSONNEL FILE (ESC = CANCEL)", True, GREEN), (50, 50))
        y = 110
        prompts_iter = iter(reg_prompts)
        for idx, ans in enumerate(reg_answers):
            p_text = next(prompts_iter)
            shown = "*" * len(ans) if idx == 1 else (ans if ans.strip() else "[Skipped]")
            screen.blit(font.render(f"{p_text} {shown}", True, GRAY), (50, y))
            y += 30
        curr_prompt = next(prompts_iter)
        screen.blit(font.render(curr_prompt, True, GREEN), (50, y + 15))
        curr_display = "*" * len(input_buffer) if reg_step == 1 else input_buffer
        screen.blit(font.render(f"> {curr_display}_", True, GREEN), (50, y + 50))

    elif state == "TERMINAL":
        header = f"USER: {current_user.get('name')} | LVL: {current_user.get('clearance')} | SITE: {current_user.get('site')} | LANG: {lang.upper()}"
        pygame.draw.rect(screen, (20, 40, 28), (0, 0, WIDTH, 40))
        screen.blit(font.render(header, True, theme), (20, 10))

        y = 55 + scroll_y
        for line in terminal_lines:
            if 35 < y < HEIGHT - 50:
                col = RED if "ACCESS DENIED" in line or "ERROR" in line else theme
                screen.blit(font.render(line, True, col), (20, y))
            y += 26

        pygame.draw.rect(screen, BG, (0, HEIGHT - 45, WIDTH, 45))
        pygame.draw.line(screen, theme, (0, HEIGHT - 45), (WIDTH, HEIGHT - 45), 2)
        screen.blit(font.render(f"SCiPNET > {input_buffer}_", True, theme), (20, HEIGHT - 32))

    pygame.display.flip()
    pygame.time.delay(16)
