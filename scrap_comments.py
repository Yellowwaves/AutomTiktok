import asyncio
import os
from TikTokApi import TikTokApi

# Identifiants vidéo et token
video_id = "7248300636498890011"  # ID de la vidéo TikTok
ms_token = os.environ.get("ms_token", None)  # Assurez-vous que le token est défini dans les variables d'environnement

# Fonction principale pour récupérer les commentaires
async def get_comments():
    # Liste pour stocker les commentaires
    comments_list = []

    # Initialisation de l'API
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(id=video_id)

        # Limiter le nombre de commentaires récupérés
        async for comment in video.comments(count=2):  # Réduit à 2 commentaires pour le test
            comments_list.append({
                "id": comment.id,
                "username": comment.author.username,
                "text": comment.text,
                "likes_count": comment.likes_count,
            })

    return comments_list

if __name__ == "__main__":
    comments = asyncio.run(get_comments())

    # Stocker les commentaires dans une variable ligne par ligne
    comments_text = ""
    for idx, comment in enumerate(comments):
        comment_line = f"Commentaire {idx + 1}:\n"
        comment_line += f"  ID: {comment['id']}\n"
        comment_line += f"  Utilisateur: {comment['username']}\n"
        comment_line += f"  Texte: {comment['text']}\n"
        comment_line += f"  J'aime: {comment['likes_count']}\n\n"
        comments_text += comment_line

    # Écrire les commentaires dans un fichier texte
    with open("comments.txt", "w", encoding="utf-8") as file:
        file.write(comments_text)

    # Afficher les commentaires pour vérification
    print("Commentaires stockés dans 'comments.txt':")
    print(comments_text)
