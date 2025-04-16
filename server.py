from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, send_file
import io
import os

def normalize_name(nombre, apellidos):
    nombre = nombre.strip().title()
    apellidos = apellidos.strip().title()

    nombre_parts = nombre.split()
    apellido_parts = apellidos.split()

    if not apellidos:
        # If there's no apellido, try to get first two words from nombre
        if len(nombre_parts) >= 2:
            words = " ".join([nombre_parts[0], nombre_parts[1]])
        else:
            words = nombre_parts[0] if nombre_parts else ""
    else:
        primer_nombre = nombre_parts[0] if nombre_parts else ""
        primer_apellido = apellido_parts[0] if apellido_parts else ""
        if primer_apellido and primer_apellido != primer_nombre:
            words = " ".join([primer_nombre, primer_apellido])
        else:
            words = primer_nombre

    return words

def generate_image(name, last_name):
    # Load the template image
    try:
        image_path = os.path.join("1x", "Imagen.png")
        image = Image.open(image_path) 
        draw = ImageDraw.Draw(image)
    except IOError:
        raise RuntimeError("Image file not found or could not be loaded. Please check the font path.")  
    # Create a drawing context

    # Load a font (adjust path if needed)
    try:
        font_path = os.path.join("static", "futur.ttf")
        font = ImageFont.truetype(font_path, 120)
    except IOError:
        raise RuntimeError("Font file not found or could not be loaded. Please check the font path.")

    # Normalize the name and last name
    full_name = normalize_name(name, last_name)

    # Get image dimensions
    img_width, img_height = image.size

    # Calculate text size
    text_bbox = draw.textbbox((0, 0), full_name, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Calculate text position to center it
    text_position = ((img_width - text_width) // 2, 540)

    # Define text color (white in this example)
    text_color = (169, 44, 42)

    # Add text to image
    draw.text(text_position, full_name, font=font, fill=text_color)

    # Save the personalized ticket
    # Save image in memory
    img_io = io.BytesIO()
    image.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

app = Flask(__name__)

@app.route('/image')
def serve_image():
    name = request.args.get("name", "")
    last_name = request.args.get("lastname", "")
    
    img_io = generate_image(name, last_name)
    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)