import os
from PIL import Image, ImageDraw, ImageFont

def draw_organigrama():
    # Size of the image
    width, height = 1000, 600
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Try loading a font, otherwise use default
    try:
        # Use a common system font
        font = ImageFont.truetype("arial.ttf", 14)
        font_title = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Draw boxes function
    def draw_box(text_lines, x1, y1, x2, y2, fill_color, border_color):
        draw.rectangle([x1, y1, x2, y2], fill=fill_color, outline=border_color, width=2)
        y_offset = y1 + 10
        for line in text_lines:
            # Get text size
            text_w = draw.textlength(line, font=font)
            x_pos = x1 + (x2 - x1 - text_w) / 2
            draw.text((x_pos, y_offset), line, fill="black", font=font)
            y_offset += 20

    # Colors
    bg_director = (217, 226, 243) # light blue
    bg_coor = (230, 240, 230) # light green
    bg_specialists = (252, 228, 214) # light orange
    bg_beneficiaries = (242, 242, 242) # light grey
    border_color = (31, 73, 125) # dark blue

    # Coordinates
    # Director Box
    draw_box(["Director de la Fundación", "(Administración y Auditoría)"], 375, 30, 625, 90, bg_director, border_color)

    # Connecting lines
    draw.line([(500, 90), (500, 150)], fill=border_color, width=2)
    draw.line([(200, 150), (800, 150)], fill=border_color, width=2)

    # Coordinadores Box
    draw_box(["Coordinadores de Equipos", "(Supervisión de Casos)"], 100, 180, 300, 240, bg_coor, border_color)
    draw.line([(200, 150), (200, 180)], fill=border_color, width=2)

    # Equipos Multidisciplinarios Box
    draw_box(["Equipos de Restitución", "(Abogado, Médico, Psicólogo, TS)"], 600, 180, 850, 240, bg_specialists, border_color)
    draw.line([(725, 150), (725, 180)], fill=border_color, width=2)

    # Connect Coordinadores to Specialists
    draw.line([(300, 210), (600, 210)], fill=border_color, width=2)

    # Draw specialist roles branching from Specialists box
    draw.line([(725, 240), (725, 300)], fill=border_color, width=2)
    draw.line([(450, 300), (1000, 300)], fill=border_color, width=2)

    # Abogado
    draw_box(["Abogado", "(Valoración Jurídica)"], 375, 330, 525, 380, bg_specialists, border_color)
    draw.line([(450, 300), (450, 330)], fill=border_color, width=2)

    # Médico
    draw_box(["Médico", "(Valoración Física y Salud)"], 535, 330, 685, 380, bg_specialists, border_color)
    draw.line([(610, 300), (610, 330)], fill=border_color, width=2)

    # Psicólogo
    draw_box(["Psicólogo", "(Valoración Emocional)"], 695, 330, 845, 380, bg_specialists, border_color)
    draw.line([(770, 300), (770, 330)], fill=border_color, width=2)

    # Trabajador Social
    draw_box(["Trabajador Social", "(Entorno Socio-familiar)"], 855, 330, 1005, 380, bg_specialists, border_color)
    draw.line([(930, 300), (930, 330)], fill=border_color, width=2)

    # Connect Director to Beneficiaries directly
    # Draw line from Director down on the right or middle
    # Let's draw it from 500 down to 430
    draw.line([(500, 90), (500, 410)], fill=border_color, width=2)
    draw.line([(500, 410), (500, 430)], fill=border_color, width=2)

    # Beneficiarios Box
    draw_box(["Beneficiarios", "(Niñas, Niños y Adolescentes - NNA)"], 375, 430, 625, 490, bg_beneficiaries, border_color)

    # Connect Beneficiaries to Tutores
    draw.line([(500, 490), (500, 520)], fill=border_color, width=2)
    draw_box(["Tutores y Familiares", "(Red de Apoyo Primaria)"], 375, 520, 625, 570, bg_beneficiaries, border_color)

    # Save image
    output_dir = "CDT-Analysis/images"
    os.makedirs(output_dir, exist_ok=True)
    img_path = os.path.join(output_dir, "organigrama_fundacion.png")
    img.save(img_path)
    print(f"Organigrama saved successfully to {img_path}!")

if __name__ == "__main__":
    draw_organigrama()
