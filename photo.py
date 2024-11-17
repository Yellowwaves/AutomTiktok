import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
from TikTokApi import TikTokApi

# Identifiants vidéo et token
video_id = "7248300636498890011"  # ID de la vidéo TikTok
ms_token = os.environ.get("ms_token", None)  # Assurez-vous que le token est défini dans les variables d'environnement

# Fonction pour créer une image de commentaire TikTok
def create_tiktok_comment_image(username, text, likes_count, output_path):
    # Dimensions de l'image
    img_width, img_height = 500, 200
    bg_color = (255, 255, 255)  # Blanc
    text_color = (0, 0, 0)  # Noir

    # Créer une image vierge
    img = Image.new("RGB", (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Charger une police
    font_path = "arial.ttf"  # Assurez-vous que cette police est installée ou remplacez-la par une autre
    if not os.path.exists(font_path):
        raise FileNotFoundError("Police non trouvée. Téléchargez 'arial.ttf' ou utilisez une police disponible.")

    font = ImageFont.truetype(font_path, size=20)

    # Dessiner les éléments du commentaire
    profile_pic_diameter = 50
    padding = 10
    draw.ellipse(
        (padding, padding, profile_pic_diameter + padding, profile_pic_diameter + padding),
        fill=(200, 200, 200),
    )  # Cercle pour l'avatar

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

# Fonction principale pour récupérer les commentaires
async def get_comments():
    # Liste pour stocker les commentaires
    comments_list = []

    # Initialisation de l'API
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(id=video_id)

        # Limiter le nombre de commentaires récupérés
        async for comment in video.comments(count=5):  # Modifier le count pour ajuster le nombre de commentaires
            comments_list.append({
                "id": comment.id,
                "username": comment.author.username,
                "text": comment.text,
                "likes_count": comment.likes_count,
            })

    return comments_list

if __name__ == "__main__":
    # Récupérer les commentaires et créer une image pour chacun
    comments = asyncio.run(get_comments())
    output_folder = "comments_images"
    os.makedirs(output_folder, exist_ok=True)

    for idx, comment in enumerate(comments):
        output_path = os.path.join(output_folder, f"comment_{idx + 1}.png")
        create_tiktok_comment_image(
            username=comment["username"],
            text=comment["text"],
            likes_count=comment["likes_count"],
            output_path=output_path,
        )
