import os
from PIL import Image, ImageDraw, ImageFont

def draw_navigation_map():
    width, height = 1000, 600
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 12)
        font_title = ImageFont.truetype("arial.ttf", 13)
    except IOError:
        font = ImageFont.load_default()
        font_title = ImageFont.load_default()

    def draw_node(text_lines, x, y, w, h, bg_color):
        border_color = (31, 73, 125)
        draw.rectangle([x, y, x+w, y+h], fill=bg_color, outline=border_color, width=2)
        y_offset = y + (h - len(text_lines)*16)/2
        for line in text_lines:
            text_w = draw.textlength(line, font=font)
            draw.text((x + (w - text_w)/2, y_offset), line, fill="black", font=font)
            y_offset += 16

    # Colors
    color_login = (217, 226, 243) # light blue
    color_director = (230, 240, 230) # light green
    color_coordinador = (252, 228, 214) # light orange
    color_especialista = (255, 242, 204) # light yellow
    border_color = (31, 73, 125)

    # 1. Login Screen (Root)
    draw_node(["Login (IU-01)", "Email / Contraseña"], 400, 30, 200, 50, color_login)

    # Connecting lines from Login to dashboards
    draw.line([(500, 80), (500, 140)], fill=border_color, width=2)
    draw.line([(150, 140), (850, 140)], fill=border_color, width=2)

    # Director Branch
    draw.line([(150, 140), (150, 180)], fill=border_color, width=2)
    draw_node(["Director Dashboard (IU-02)", "Gestión de Personal"], 50, 180, 200, 50, color_director)
    # Sub-pages of Director
    draw.line([(150, 230), (150, 280)], fill=border_color, width=2)
    draw.line([(50, 280), (250, 280)], fill=border_color, width=2)
    
    draw.line([(50, 280), (50, 310)], fill=border_color, width=2)
    draw_node(["Registrar Personal", "(IU-03)"], 10, 310, 130, 45, color_director)
    
    draw.line([(150, 280), (150, 310)], fill=border_color, width=2)
    draw_node(["Equipos Panel", "(IU-04)"], 150, 310, 120, 45, color_director)
    
    draw.line([(250, 280), (250, 310)], fill=border_color, width=2)
    draw_node(["Crear Equipo", "(IU-05)"], 280, 310, 110, 45, color_director)

    # Coordinador Branch
    draw.line([(500, 140), (500, 180)], fill=border_color, width=2)
    draw_node(["Coordinador Dashboard (IU-06)", "Gestión de Expedientes"], 400, 180, 200, 50, color_coordinador)
    # Sub-pages of Coordinador
    draw.line([(500, 230), (500, 280)], fill=border_color, width=2)
    draw.line([(450, 280), (590, 280)], fill=border_color, width=2)
    
    draw.line([(450, 280), (450, 310)], fill=border_color, width=2)
    draw_node(["Registrar NNA (FUD)", "(IU-07)"], 400, 310, 140, 45, color_coordinador)
    
    draw.line([(590, 280), (590, 310)], fill=border_color, width=2)
    draw_node(["Asignar Expediente", "(IU-08)"], 550, 310, 140, 45, color_coordinador)

    # Especialista Branch
    draw.line([(850, 140), (850, 180)], fill=border_color, width=2)
    draw_node(["Especialista Dashboard (IU-09)", "Mis Expedientes Asignados"], 750, 180, 200, 50, color_especialista)
    # Sub-pages of Especialista
    draw.line([(850, 230), (850, 280)], fill=border_color, width=2)
    draw.line([(760, 280), (940, 280)], fill=border_color, width=2)
    
    draw.line([(760, 280), (760, 310)], fill=border_color, width=2)
    draw_node(["Registrar Valoración", "(IU-10)"], 700, 310, 140, 45, color_especialista)
    
    draw.line([(940, 280), (940, 310)], fill=border_color, width=2)
    draw_node(["Carga Documental", "(IU-11)"], 860, 310, 130, 45, color_especialista)

    # General arrows indicating redirect back to Login (Logout)
    draw.text((300, 100), "<--- Logout", fill=(128, 128, 128), font=font)
    draw.text((650, 100), "Logout --->", fill=(128, 128, 128), font=font)

    # Save
    os.makedirs("CDT-Analysis/images", exist_ok=True)
    img_path = "CDT-Analysis/images/mapa_navegacion_taimotla.png"
    img.save(img_path)
    print(f"Navigation map saved successfully to {img_path}!")

if __name__ == "__main__":
    draw_navigation_map()
