from PIL import Image, ImageDraw, ImageFont
import os

# Fonction pour créer une image de commentaire TikTok
def create_tiktok_comment_image(username, text, likes_count, output_path):
    # Dimensions de l'image
    img_width, img_height = 500, 200
    bg_color = (255, 255, 255)  # Blanc
    text_color = (0, 0, 0)  # Noir

    # Créer une image vierge
    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Charger une police
    font_path = "arial.ttf"  # Assurez-vous que cette police est installée ou remplacez-la par une autre
    if not os.path.exists(font_path):
        raise FileNotFoundError("Police non trouvée. Téléchargez 'arial.ttf' ou utilisez une police disponible.")

    font = ImageFont.truetype(font_path, size=20)

    # Dessiner les éléments du commentaire
    profile_pic_diameter = 50
    padding = 10
    draw.ellipse((padding, padding, profile_pic_diameter + padding, profile_pic_diameter + padding), fill=(200, 200, 200))  # Cercle pour l'avatar

    # Texte du pseudo
    draw.text((padding * 2 + profile_pic_diameter, padding), username, fill=text_color, font=font)

    # Texte du commentaire
    comment_x = padding * 2 + profile_pic_diameter
    comment_y = padding + 30
    draw.text((comment_x, comment_y), text, fill=text_color, font=font)

    # Texte des likes
    likes_text = f"❤️ {likes_count}"
    draw.text((img_width - padding - 100, img_height - padding - 30), likes_text, fill=text_color, font=font)

    # Sauvegarder l'image
    img.save(output_path)
    print(f"Image de commentaire créée : {output_path}")

# Exemple d'utilisation
if __name__ == "__main__":
    username = "example_user"
    text = "Ceci est un exemple de commentaire TikTok !"
    likes_count = 250
    output_path = "comment_example.png"
    create_tiktok_comment_image(username, text, likes_count, output_path)
