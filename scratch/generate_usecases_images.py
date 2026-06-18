import os
from PIL import Image, ImageDraw, ImageFont

def draw_usecase_diagrams():
    # Colors
    bg_color = (255, 255, 255)
    border_color = (31, 73, 125)
    usecase_color = (217, 226, 243)
    text_color = (0, 0, 0)

    try:
        font = ImageFont.truetype("arial.ttf", 12)
        font_title = ImageFont.truetype("arial.ttf", 13)
    except IOError:
        font = ImageFont.load_default()
        font_title = ImageFont.load_default()

    def draw_actor(draw, name, x, y):
        # Head
        draw.ellipse([(x-10, y-30), (x+10, y-10)], outline=border_color, width=2)
        # Body
        draw.line([(x, y-10), (x, y+15)], fill=border_color, width=2)
        # Arms
        draw.line([(x-20, y), (x+20, y)], fill=border_color, width=2)
        # Legs
        draw.line([(x, y+15), (x-15, y+35)], fill=border_color, width=2)
        draw.line([(x, y+15), (x+15, y+35)], fill=border_color, width=2)
        # Label
        lines = name.split("\n")
        y_offset = y + 40
        for line in lines:
            text_w = draw.textlength(line, font=font)
            draw.text((x - text_w/2, y_offset), line, fill=text_color, font=font)
            y_offset += 16

    def draw_usecase_ellipse(draw, label, x, y, w, h):
        draw.ellipse([(x, y), (x+w, y+h)], fill=usecase_color, outline=border_color, width=2)
        lines = label.split("\n")
        y_offset = y + (h - len(lines)*16)/2
        for line in lines:
            text_w = draw.textlength(line, font=font)
            draw.text((x + (w - text_w)/2, y_offset), line, fill=text_color, font=font)
            y_offset += 16

    # 1. General Use Case Diagram (casosDeUso.png)
    img1 = Image.new("RGB", (700, 450), "white")
    draw1 = ImageDraw.Draw(img1)
    
    # Draw System Boundary
    draw1.rectangle([180, 20, 520, 420], outline=border_color, width=2)
    draw1.text((190, 30), "Taimotla - Restitución de Derechos", fill=border_color, font=font_title)

    # Draw Actors
    draw_actor(draw1, "Director", 80, 150)
    draw_actor(draw1, "Coordinador", 80, 320)
    draw_actor(draw1, "Especialista", 620, 230)

    # Draw Use Cases
    draw_usecase_ellipse(draw1, "CU-01\nControl de acceso", 240, 60, 200, 70)
    draw_usecase_ellipse(draw1, "CU-02\nGestión de usuarios\ny roles", 240, 150, 200, 70)
    draw_usecase_ellipse(draw1, "CU-03\nGestión de expediente\ndel NNA", 240, 240, 200, 70)
    draw_usecase_ellipse(draw1, "CU-04\nAsignación de casos", 240, 330, 200, 70)

    # Draw Association Lines
    # Director to CU-01, CU-02
    draw1.line([(100, 150), (240, 95)], fill=border_color, width=1)
    draw1.line([(100, 150), (240, 185)], fill=border_color, width=1)
    
    # Coordinador to CU-01, CU-03, CU-04
    draw1.line([(100, 320), (240, 95)], fill=border_color, width=1)
    draw1.line([(100, 320), (240, 275)], fill=border_color, width=1)
    draw1.line([(100, 320), (240, 365)], fill=border_color, width=1)

    # Especialista to CU-01, CU-03
    draw1.line([(600, 230), (440, 95)], fill=border_color, width=1)
    draw1.line([(600, 230), (440, 275)], fill=border_color, width=1)

    # Save casesDeUso.png
    os.makedirs("CDT-Analysis/images", exist_ok=True)
    img1.save("CDT-Analysis/images/casosDeUso.png")
    print("casosDeUso.png saved successfully!")

    # 2. Detailed Diagram (casosDeUsoDetalle.png)
    # Since we rotate it in LaTeX [angle=90], we can draw it landscape or portrait. Let's make it 900x600.
    img2 = Image.new("RGB", (900, 600), "white")
    draw2 = ImageDraw.Draw(img2)
    
    # System boundary
    draw2.rectangle([200, 30, 700, 570], outline=border_color, width=2)
    draw2.text((210, 40), "Módulo de Casos - Detalles", fill=border_color, font=font_title)

    draw_actor(draw2, "Director", 80, 180)
    draw_actor(draw2, "Coordinador", 80, 400)
    draw_actor(draw2, "Especialistas\n(Abogado, Médico, Psi, TS)", 820, 290)

    # Detail Use Cases
    draw_usecase_ellipse(draw2, "CU-01\nControl de acceso", 350, 50, 200, 65)
    draw_usecase_ellipse(draw2, "CU-02.1\nRegistrar usuario", 350, 130, 200, 65)
    draw_usecase_ellipse(draw2, "CU-02.2\nEditar/Deshabilitar\nusuario", 350, 210, 200, 65)
    draw_usecase_ellipse(draw2, "CU-03.1\nRegistrar NNA\n(FUD)", 350, 290, 200, 65)
    draw_usecase_ellipse(draw2, "CU-03.2\nSubir documentos\n(Acta/Cartilla)", 350, 370, 200, 65)
    draw_usecase_ellipse(draw2, "CU-03.3\nRegistrar valoración\n(Med/Psi/TS/Jur)", 350, 450, 200, 65)
    draw_usecase_ellipse(draw2, "CU-04\nAsignar caso\na equipo", 350, 530, 200, 65)

    # Connections
    # Director to CU-01, CU-02.1, CU-02.2
    draw2.line([(100, 180), (350, 82)], fill=border_color, width=1)
    draw2.line([(100, 180), (350, 162)], fill=border_color, width=1)
    draw2.line([(100, 180), (350, 242)], fill=border_color, width=1)
    
    # Coordinador to CU-01, CU-03.1, CU-03.3, CU-04
    draw2.line([(100, 400), (350, 82)], fill=border_color, width=1)
    draw2.line([(100, 400), (350, 322)], fill=border_color, width=1)
    draw2.line([(100, 400), (350, 482)], fill=border_color, width=1)
    draw2.line([(100, 400), (350, 562)], fill=border_color, width=1)

    # Specialists to CU-01, CU-03.2, CU-03.3
    draw2.line([(800, 290), (550, 82)], fill=border_color, width=1)
    draw2.line([(800, 290), (550, 402)], fill=border_color, width=1)
    draw2.line([(800, 290), (550, 482)], fill=border_color, width=1)

    img2.save("CDT-Analysis/images/casosDeUsoDetalle.png")
    print("casosDeUsoDetalle.png saved successfully!")

if __name__ == "__main__":
    draw_usecase_diagrams()
