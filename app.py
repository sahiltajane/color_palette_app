from flask import Flask, render_template, request
import random

app = Flask(__name__)

def hex_to_rgb(hex_color):
    """Convert a hex color string (e.g., #ff5733) to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def adjust_brightness(color, factor):
    """Adjust brightness of a color by a given factor (for light/dark)."""
    return [min(max(int(c * factor), 0), 255) for c in color]

def generate_shaded_palette(base_color, num_shades, shade_type):
    """Generate light or dark shaded colors from a base color."""
    shades = []
    
    # Define how much to change brightness per step
    if shade_type == 'light':
        step_factor = 1 + (1.0 / num_shades)  # Lighten the color
    elif shade_type == 'dark':
        step_factor = 1 - (1.0 / num_shades)  # Darken the color
    else:
        step_factor = None  # Will handle both
    
    for i in range(num_shades):
        if shade_type == 'both':
            if i < num_shades // 2:
                # Light shades
                factor = 1 + (i / (num_shades // 2)) * 0.5  # Lighter towards 255
            else:
                # Dark shades
                factor = 1 - ((i - num_shades // 2) / (num_shades // 2)) * 0.5  # Darker towards 0
        else:
            factor = 1 + i * (step_factor - 1)  # Single direction (light or dark)
        
        shaded_color = adjust_brightness(base_color, factor)
        shades.append(f'rgb({shaded_color[0]}, {shaded_color[1]}, {shaded_color[2]})')
    
    return shades

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_colors = int(request.form['num_colors'])
        palette_type = request.form.get('palette_type', 'random')
        shade_type = request.form.get('shade_type', 'both')
        base_color_hex = request.form.get('base_color', '#ff0000')  # Default color red
        
        # Convert the base color from hex to RGB
        base_color = hex_to_rgb(base_color_hex)
        
        if palette_type == 'random':
            # Generate random colors
            colors = [f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})' for _ in range(num_colors)]
        else:
            # Generate shaded palette based on the user-selected base color
            colors = generate_shaded_palette(base_color, num_colors, shade_type)
        
        return render_template('index.html', colors=colors, num_colors=num_colors, palette_type=palette_type, shade_type=shade_type)
    
    return render_template('index.html', colors=[], num_colors=0)

if __name__ == "__main__":
    app.run(debug=True)
