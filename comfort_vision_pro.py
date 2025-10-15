"""
EyeZen - Filtros de Conforto Visual
Lucas Andrade Desenvolvimento de Softwares
Versão Profissional com Sistema de Bandeja
"""

import FreeSimpleGUI as sg
import ctypes
import numpy as np
import os
import json
import pystray
from PIL import Image, ImageDraw
from pynput import keyboard
import threading
import sys

# --- Configurações ---
FILTER_FILE = "last_filter.json"
LOGO_PATH = r"C:\Users\LucasRafaeldeAndrade\Desktop\Repositorios\EyeZen\imagens\eyezen.ico"

FILTERS = {
    # Filtros de Conforto (lado esquerdo)
    "🌙 Noturno Suave": (0.95, 1.0, 0.85),      # Levemente amarelado
    "🟢 Leitura Verde": (0.88, 1.0, 0.88),      # Verde suave bilateral
    "🟡 Papel Creme": (1.0, 0.98, 0.85),        # Tom creme/papel antigo
    "🔘 Desativado": (1.0, 1.0, 1.0),           # Normal
    
    # Filtros Especiais (lado direito)
    "☀️ Fique Acordado": (0.95, 1.0, 1.15),     # Mais azul = alerta
    "🌈 Modo Feliz": (1.08, 1.05, 1.02),        # Cores mais vivas
    "💜 Modo Crepúsculo": (1.0, 0.88, 1.05),    # Roxo suave relaxante
    "🎨 Sépia Clássico": (1.0, 0.95, 0.82)      # Sépia fotográfico
}

# Atalhos globais: Ctrl+Alt+[1-8]
HOTKEYS = {
    "<ctrl>+<alt>+1": "🌙 Noturno Suave",
    "<ctrl>+<alt>+2": "🟢 Leitura Verde",
    "<ctrl>+<alt>+3": "🟡 Papel Creme",
    "<ctrl>+<alt>+4": "🔘 Desativado",
    "<ctrl>+<alt>+5": "☀️ Fique Acordado",
    "<ctrl>+<alt>+6": "🌈 Modo Feliz",
    "<ctrl>+<alt>+7": "💜 Modo Crepúsculo",
    "<ctrl>+<alt>+8": "🎨 Sépia Clássico"
}

# Atalhos globais: Ctrl+Alt+[1-8]
HOTKEYS = {
    "<ctrl>+<alt>+1": "🌙 Noturno Suave",
    "<ctrl>+<alt>+2": "🟢 Leitura Verde",
    "<ctrl>+<alt>+3": "🟡 Papel Creme",
    "<ctrl>+<alt>+4": "🔘 Desativado",
    "<ctrl>+<alt>+5": "☀️ Fique Acordado",
    "<ctrl>+<alt>+6": "🌑 Dark Mode",
    "<ctrl>+<alt>+7": "📖 Modo Kindle",
    "<ctrl>+<alt>+8": "🎨 Sépia Clássico"
}

# --- Variáveis globais ---
current_filter = "🔘 Desativado"
main_window = None
tray_icon = None
dark_mode_active = False  # Flag para Dark Mode

# --- Funções de Gamma ---
# --- Funções de Gamma ---
def set_gamma(r_gain, g_gain, b_gain):
    """Aplica o filtro de gamma na tela"""
    try:
        ramp = np.linspace(0, 65535, 256).astype('uint16')
        gamma_ramp = np.zeros((3, 256), dtype='uint16')
        
        gamma_ramp[0] = np.clip(ramp * r_gain, 0, 65535).astype('uint16')
        gamma_ramp[1] = np.clip(ramp * g_gain, 0, 65535).astype('uint16')
        gamma_ramp[2] = np.clip(ramp * b_gain, 0, 65535).astype('uint16')
        
        ramp_ptr = gamma_ramp.flatten().ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
        hdc = ctypes.windll.user32.GetDC(0)
        result = ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ramp_ptr)
        ctypes.windll.user32.ReleaseDC(0, hdc)
        
        return result != 0
    except Exception as e:
        print(f"Erro ao aplicar filtro: {e}")
        return False

def save_filter(filter_name):
    """Salva o último filtro usado"""
    try:
        with open(FILTER_FILE, "w") as f:
            json.dump({"last": filter_name}, f)
    except Exception:
        pass

def load_last_filter():
    """Carrega o último filtro usado"""
    if os.path.exists(FILTER_FILE):
        try:
            with open(FILTER_FILE, "r") as f:
                data = json.load(f)
                return data.get("last", "🔘 Desativado")
        except Exception:
            pass
    return "🔘 Desativado"

def apply_filter(filter_name):
    """Aplica um filtro específico"""
    global current_filter
    
    if filter_name in FILTERS:
        r, g, b = FILTERS[filter_name]
        if set_gamma(r, g, b):
            current_filter = filter_name
            save_filter(filter_name)
            update_tray_menu()
            return True
    
    return False

# --- Sistema de Bandeja ---
def create_icon_image():
    """Cria um ícone para a bandeja (ou usa a logo se disponível)"""
    if os.path.exists(LOGO_PATH):
        try:
            return Image.open(LOGO_PATH)
        except Exception:
            pass
    
    # Ícone padrão (círculo verde)
    img = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill='#00AA00', outline='#006600', width=3)
    return img

def update_tray_menu():
    """Atualiza o menu da bandeja com o filtro atual"""
    global tray_icon
    if tray_icon:
        tray_icon.menu = create_tray_menu()
        tray_icon.update_menu()

def create_tray_menu():
    """Cria o menu da bandeja do sistema"""
    menu_items = []
    
    # Adiciona filtros com indicador do filtro atual
    for filter_name in FILTERS.keys():
        prefix = "✓ " if filter_name == current_filter else "   "
        menu_items.append(
            pystray.MenuItem(
                f"{prefix}{filter_name}",
                lambda _, f=filter_name: apply_filter(f)
            )
        )
    
    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(pystray.MenuItem("Abrir Painel", show_window))
    menu_items.append(pystray.MenuItem("Sobre", show_about))
    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(pystray.MenuItem("Sair", quit_app))
    
    return pystray.Menu(*menu_items)

def show_window(icon=None, item=None):
    """Mostra a janela principal"""
    global main_window
    if main_window:
        main_window.un_hide()
        main_window.bring_to_front()

def show_about(icon=None, item=None):
    """Mostra informações sobre o aplicativo"""
    sg.popup(
        "EyeZen - Filtros de Conforto Visual\n\n"
        "Versão 2.0 - Profissional\n"
        "Lucas Andrade Desenvolvimento de Softwares\n\n"
        "Atalhos Globais:\n"
        "Conforto:\n"
        "• Ctrl+Alt+1: Noturno Suave\n"
        "• Ctrl+Alt+2: Leitura Verde\n"
        "• Ctrl+Alt+3: Papel Creme\n"
        "• Ctrl+Alt+4: Desativado\n\n"
        "Especiais:\n"
        "• Ctrl+Alt+5: Fique Acordado\n"
        "• Ctrl+Alt+6: Modo Feliz\n"
        "• Ctrl+Alt+7: Modo Crepúsculo\n"
        "• Ctrl+Alt+8: Sépia Clássico",
        title="Sobre",
        icon=LOGO_PATH if os.path.exists(LOGO_PATH) else None
    )

def quit_app(icon=None, item=None):
    """Encerra o aplicativo"""
    global tray_icon, main_window
    
    # Restaura gamma normal
    set_gamma(1.0, 1.0, 1.0)
    
    # Fecha a bandeja
    if tray_icon:
        tray_icon.stop()
    
    # Fecha a janela
    if main_window:
        main_window.close()
    
    sys.exit(0)

def run_tray_icon():
    """Executa o ícone da bandeja em thread separada"""
    global tray_icon
    icon_image = create_icon_image()
    tray_icon = pystray.Icon(
        "comfort_vision",
        icon_image,
        "EyeZen - Filtros de Conforto Visual",
        menu=create_tray_menu()
    )
    tray_icon.run()

# --- Atalhos Globais ---
def setup_hotkeys():
    """Configura os atalhos globais de teclado"""
    def on_activate(filter_name):
        def callback():
            apply_filter(filter_name)
        return callback
    
    listener = keyboard.GlobalHotKeys({
        hotkey: on_activate(filter_name)
        for hotkey, filter_name in HOTKEYS.items()
    })
    listener.start()

# --- Interface Gráfica ---
def create_main_window():
    """Cria a janela principal"""
    sg.theme("DarkGrey5")
    
    # Cores dos botões
    btn_size = (18, 2)
    
    layout = [
        [sg.Text("EyeZen - Filtros de Conforto Visual", font=("Inter", 14, "bold"), 
                 justification="center", expand_x=True, pad=(0, 10))],
        [sg.Text("Lucas Andrade Desenvolvimento de Softwares", font=("Cascadia Code", 9), 
                 justification="center", expand_x=True, text_color="lightgray")],
        [sg.HorizontalSeparator(pad=(0, 15))],
        
        # Títulos das colunas
        [sg.Text("Conforto", font=("Roboto", 11, "bold"), 
                 size=(20, 1), justification="center"),
         sg.Text("Especiais", font=("Roboto", 11, "bold"), 
                 size=(20, 1), justification="center")],
        
        # Linha 1
        [sg.Button("🌙 Noturno Suave", size=btn_size, key="🌙 Noturno Suave",
                   button_color=("white", "#5D4E37")),
         sg.Button("☀️ Fique Acordado", size=btn_size, key="☀️ Fique Acordado",
                   button_color=("white", "#0077BE"))],
        
        # Linha 2
        [sg.Button("🟢 Leitura Verde", size=btn_size, key="🟢 Leitura Verde",
                   button_color=("white", "#2E7D32")),
         sg.Button("🌈 Modo Feliz", size=btn_size, key="🌈 Modo Feliz",
                   button_color=("white", "#E91E63"))],
        
        # Linha 3
        [sg.Button("🟡 Papel Creme", size=btn_size, key="🟡 Papel Creme",
                   button_color=("white", "#8B7355")),
         sg.Button("💜 Modo Crepúsculo", size=btn_size, key="💜 Modo Crepúsculo",
                   button_color=("white", "#6A1B9A"))],
        
        # Linha 4
        [sg.Button("🔘 Desativado", size=btn_size, key="🔘 Desativado",
                   button_color=("white", "#424242")),
         sg.Button("🎨 Sépia Clássico", size=btn_size, key="🎨 Sépia Clássico",
                   button_color=("white", "#704214"))],
        
        [sg.HorizontalSeparator(pad=(0, 15))],
        
        [sg.Text("Atalhos: Ctrl+Alt+1 a 8", font=("Segoe UI", 9), 
                 text_color="lightgray", justification="center", expand_x=True)],
        
        [sg.Button("Minimizar para Bandeja", size=(19, 1), 
                   button_color=("white", "#1976D2"), key="Minimize"),
         sg.Button("Sair", size=(19, 1), 
                   button_color=("white", "#C62828"), key="Exit")]
    ]
    
    window = sg.Window(
        "EyeZen - Filtros de Conforto Visual",
        layout,
        element_justification="center",
        finalize=True,
        resizable=False,
        icon="imagens/eyezen.ico",
        location=(None, None)
    )

    
    return window

def main():
    """Função principal do aplicativo"""
    global main_window
    
    # Aplica o último filtro usado
    last_filter = load_last_filter()
    apply_filter(last_filter)
    
    # Inicia o ícone da bandeja em thread separada
    tray_thread = threading.Thread(target=run_tray_icon, daemon=True)
    tray_thread.start()
    
    # Configura atalhos globais
    setup_hotkeys()
    
    # Cria a janela principal
    main_window = create_main_window()
    
    
    
    # Loop de eventos
    while True:
        event, values = main_window.read()
        
        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == "Minimize":
            # Minimiza para a bandeja ao invés de fechar
            main_window.hide()
            continue
        
        if event == sg.WINDOW_CLOSED or event == "Exit":
            quit_app()
            break
        
        # Aplicar filtros
        if event in FILTERS:
            apply_filter(event)
            sg.popup_quick_message(
                f"Filtro '{event}' aplicado!",
                background_color="#2E7D32",
                text_color="white",
                font=("Helvetica", 11),
                keep_on_top=True,
                auto_close_duration=1
            )

if __name__ == "__main__":
    main()