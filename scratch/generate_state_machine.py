import os
from PIL import Image, ImageDraw, ImageFont

def draw_state_machine():
    width, height = 900, 450
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 12)
        font_bold = ImageFont.truetype("arial.ttf", 12)
        font_title = ImageFont.truetype("arial.ttf", 13)
    except IOError:
        font = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_title = ImageFont.load_default()

    def draw_state(name, x, y, w, h):
        border_color = (31, 73, 125)
        bg_color = (242, 244, 248)
        # Rounded rectangle outline using simple polygons or drawing arc/rect
        draw.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=bg_color, outline=border_color, width=2)
        # Draw Name
        text_w = draw.textlength(name, font=font_title)
        draw.text((x + (w - text_w)/2, y + (h - 14)/2), name, fill="black", font=font_title)

    def draw_arrow(x1, y1, x2, y2, label=""):
        border_color = (112, 128, 144)
        draw.line([(x1, y1), (x2, y2)], fill=border_color, width=2)
        # Arrow head
        if x1 == x2: # vertical
            if y1 < y2: # down
                draw.polygon([(x2, y2), (x2-4, y2-8), (x2+4, y2-8)], fill=border_color)
            else: # up
                draw.polygon([(x2, y2), (x2-4, y2+8), (x2+4, y2+8)], fill=border_color)
            if label:
                draw.text((x1+8, (y1+y2)/2 - 7), label, fill="black", font=font)
        elif y1 == y2: # horizontal
            if x1 < x2: # right
                draw.polygon([(x2, y2), (x2-8, y2-4), (x2-8, y2+4)], fill=border_color)
            else: # left
                draw.polygon([(x2, y2), (x2+8, y2-4), (x2+8, y2+4)], fill=border_color)
            if label:
                text_w = draw.textlength(label, font=font)
                draw.text(((x1+x2)/2 - text_w/2, y1-16), label, fill="black", font=font)

    # Initial state circle
    draw.ellipse([(30, 200), (50, 220)], fill="black", outline="black")
    draw_arrow(50, 210, 100, 210, "Apertura caso")

    # States
    draw_state("Creado", 100, 185, 90, 50)
    draw_arrow(190, 210, 240, 210, "Asignar equipo y Acta")

    draw_state("En Diagnóstico", 240, 185, 120, 50)
    draw_arrow(360, 210, 410, 210, "Registrar valoraciones")

    draw_state("Plan Asignado", 410, 185, 120, 50)
    draw_arrow(530, 210, 580, 210, "Aprobar PRD")

    draw_state("En Ejecución", 580, 185, 110, 50)
    draw_arrow(690, 210, 740, 210, "Aplicar medidas")

    draw_state("En Seguimiento", 740, 185, 130, 50)

    # Transition from Seguimiento to Cerrado (which can go back to Creado or go down to Cerrado)
    # Let's draw Cerrado at the bottom
    draw_state("Cerrado", 740, 320, 130, 50)
    draw_arrow(805, 235, 805, 320, "Garantía total")

    # Double circle for final state at the bottom of Cerrado
    draw.ellipse([(800, 395), (820, 415)], fill="white", outline="black", width=2)
    draw.ellipse([(804, 399), (816, 411)], fill="black")
    draw_arrow(805, 370, 805, 395)

    # Transition from En Seguimiento to En Diagnóstico (if new vulnerability occurs)
    # We can draw a curved line or line with corners back
    # Let's draw it from (805, 185) up to 100, then left to 300, then down to (300, 185)
    draw.line([(805, 185), (805, 120), (300, 120), (300, 185)], fill=(112, 128, 144), width=2)
    draw.polygon([(300, 185), (296, 177), (304, 177)], fill=(112, 128, 144))
    draw.text((450, 100), "Nueva vulneración detectada", fill="black", font=font)

    # Save image
    output_dir = "CDT-Analysis/images"
    os.makedirs(output_dir, exist_ok=True)
    img_path = os.path.join(output_dir, "maquina_estados_expediente.png")
    img.save(img_path)
    print(f"State machine saved successfully to {img_path}!")

if __name__ == "__main__":
    draw_state_machine()
