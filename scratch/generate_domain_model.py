import os
from PIL import Image, ImageDraw, ImageFont

def draw_domain_model():
    width, height = 1100, 750
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 12)
        font_bold = ImageFont.truetype("arial.ttf", 12)
        font_title = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Box drawing helper
    def draw_class(name, attributes, methods, x, y, w, h, bg_color):
        border_color = (31, 73, 125)
        # Main rectangle
        draw.rectangle([x, y, x+w, y+h], fill=bg_color, outline=border_color, width=2)
        # Header separator
        draw.line([(x, y+25), (x+w, y+25)], fill=border_color, width=2)
        
        # Draw Class Name
        text_w = draw.textlength(name, font=font_title)
        draw.text((x + (w - text_w)/2, y+5), name, fill="black", font=font_title)
        
        # Draw Attributes
        y_offset = y + 30
        for attr in attributes:
            draw.text((x+8, y_offset), attr, fill="black", font=font)
            y_offset += 16
            
        # Draw separator if there are methods
        if methods:
            draw.line([(x, y_offset+4), (x+w, y_offset+4)], fill=border_color, width=1)
            y_offset += 10
            for method in methods:
                draw.text((x+8, y_offset), method, fill="black", font=font)
                y_offset += 16

    # Colors
    color_class = (242, 244, 248) # very light blue-gray
    color_core = (217, 226, 243) # light blue
    color_personal = (230, 240, 230) # light green
    border_color = (31, 73, 125)

    # 1. Persona (Superclass)
    draw_class(
        "Persona",
        ["+ curp: String [1] {PK}", "+ rfc: String [1]", "+ p_nombre: String [1]", "+ s_nombre: String [0..1]", "+ p_apellido: String [1]", "+ s_apellido: String [1]", "+ fecha_nacimiento: Date [1]", "+ id_sexo: Integer [1]", "+ id_domicilio: Integer [1]"],
        [], 50, 40, 240, 180, color_class
    )

    # 2. Personal (Subclass)
    draw_class(
        "Personal",
        ["+ fecha_alta: Date [1]", "+ voluntario: Boolean [1]", "+ contrasena: String [1]", "+ estado: Integer [1]"],
        [], 50, 290, 240, 100, color_personal
    )
    # Generalization line (Personal -> Persona)
    draw.line([(170, 290), (170, 220)], fill=border_color, width=2)
    # Triangle head at 170,220
    draw.polygon([(170, 220), (165, 230), (175, 230)], fill="white", outline=border_color)

    # 3. Director (Subclass of Personal)
    draw_class("Director", [], [], 20, 450, 120, 50, color_personal)
    draw.line([(80, 450), (80, 420), (170, 420), (170, 390)], fill=border_color, width=2)
    draw.polygon([(80, 445), (77, 450), (83, 450)], fill="white", outline=border_color)

    # 4. Coordinador (Subclass of Personal)
    draw_class("Coordinador", [], [], 170, 450, 140, 50, color_personal)
    draw.line([(240, 450), (240, 390)], fill=border_color, width=2)

    # 5. Equipo
    draw_class(
        "Equipo",
        ["+ id_equipo: Integer [1] {PK}", "+ nombre_equipo: String [1]", "+ fecha_creacion: Date [1]", "+ curp_coordinador: String [1] {FK}", "+ id_estado_equipo: Integer [1]"],
        [], 380, 290, 250, 110, color_core
    )
    # Association line (Coordinador 1 <-> 0..* Equipo)
    draw.line([(310, 470), (450, 470), (450, 400)], fill=border_color, width=2)
    draw.text((320, 455), "1", fill="black", font=font)
    draw.text((435, 405), "0..*", fill="black", font=font)

    # Association (Equipo 1 <-> 2..4 Personal/Especialista)
    draw.line([(290, 340), (380, 340)], fill=border_color, width=2)
    # Diamond head at Equipo side (380, 340) for composition/aggregation
    draw.polygon([(380, 340), (370, 335), (360, 340), (370, 345)], fill="white", outline=border_color)
    draw.text((300, 325), "2..4", fill="black", font=font)
    draw.text((350, 325), "1", fill="black", font=font)

    # 6. Expediente
    draw_class(
        "Expediente",
        ["+ id_expediente: Integer [1] {PK}", "+ num_expediente: String [1]", "+ fecha_apertura: Date [1]", "+ id_equipo_responsable: Integer [1] {FK}", "+ id_estado_expediente: Integer [1]"],
        [], 720, 290, 300, 115, color_core
    )
    # Association (Equipo 0..1 <-> 1 Expediente)
    draw.line([(630, 340), (720, 340)], fill=border_color, width=2)
    draw.text((640, 325), "0..1", fill="black", font=font)
    draw.text((705, 325), "1", fill="black", font=font)

    # 7. NNA (Niñas, Niños y Adolescentes)
    draw_class(
        "NNA",
        ["+ id_nna: Integer [1] {PK}", "+ id_persona_exp_nna: Integer [1] {FK}", "+ id_expediente: Integer [1] {FK}", "+ apodo: String [0..1]", "+ observaciones: String [0..1]", "+ id_etnia: Integer [0..1] {FK}", "+ id_nacionalidad: Integer [1] {FK}"],
        [], 720, 470, 300, 140, color_core
    )
    # Composition/Association (Expediente 1 <-> 1 NNA)
    draw.line([(870, 405), (870, 470)], fill=border_color, width=2)
    draw.polygon([(870, 405), (865, 415), (870, 425), (875, 415)], fill="black") # solid diamond for composition
    draw.text((855, 430), "1", fill="black", font=font)
    draw.text((855, 450), "1", fill="black", font=font)

    # 8. Tutor
    draw_class(
        "Tutor",
        ["+ id_tutor: Integer [1] {PK}", "+ id_persona_exp: Integer [1] {FK}", "+ ocupacion: String [1]", "+ es_sosten_economico: Boolean [1]", "+ escolaridad: String [1]", "+ patron_migracion: String [0..1]", "+ id_telefono: Integer [0..1]", "+ id_correo: Integer [0..1]", "+ id_parentesco: Integer [1]", "+ id_grado_negacion: Integer [0..1]", "+ id_grado_afectacion_emocional: Integer [0..1]"],
        [], 380, 470, 300, 200, color_class
    )
    # Association (NNA 1 <-> 1..* Tutor)
    draw.line([(680, 540), (720, 540)], fill=border_color, width=2)
    draw.text((685, 525), "1..*", fill="black", font=font)
    draw.text((708, 525), "1", fill="black", font=font)

    # 9. DocumentosNNA
    draw_class(
        "DocumentosNNA",
        ["+ id_documento_nna: Integer [1] {PK}", "+ id_nna: Integer [1] {FK}", "+ id_documento: Integer [1] {FK}", "+ id_tipo_documento: Integer [1] {FK}", "+ ruta_archivo: String [1]", "+ fecha_subida: Date [1]", "+ observaciones: String [0..1]"],
        [], 720, 40, 300, 140, color_class
    )
    # Association (NNA 1 <-> 0..* DocumentosNNA)
    draw.line([(1020, 180), (1020, 470)], fill=border_color, width=2)
    draw.text((1000, 190), "0..*", fill="black", font=font)
    draw.text((1000, 450), "1", fill="black", font=font)

    # Save image
    output_dir = "CDT-Analysis/images"
    os.makedirs(output_dir, exist_ok=True)
    img_path = os.path.join(output_dir, "modelo_dominio_fundacion.png")
    img.save(img_path)
    print(f"Domain model saved successfully to {img_path}!")

if __name__ == "__main__":
    draw_domain_model()
