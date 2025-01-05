import base64
from fastapi import HTTPException
from wordcloud import WordCloud
from io import BytesIO

def generate_wordcloud(text):
    try:
        # Validate input text
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text for word cloud is empty.")

        # Generate a word cloud
        wordcloud = WordCloud(background_color="white", width=800, height=400).generate(text)
        img = BytesIO()
        wordcloud.to_image().save(img, format="PNG")
        img_base64 = base64.b64encode(img.getvalue()).decode()

        # Return the image as a base64 string
        return img_base64

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
