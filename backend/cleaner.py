import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from fastapi import HTTPException

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_data(df, types):
    try:
        df = pd.DataFrame(df)
        df_cleaned = df.copy()

        for col, dtype in types.items():
            if col not in df_cleaned:
                raise HTTPException(status_code=400, detail=f"Column '{col}' not found in the DataFrame")

            if dtype in ["number", "rating"]:
                df_cleaned[col] = (
                    df_cleaned[col]
                    .astype(str)
                    .str.extract(r"(\d+)")
                    .apply(pd.to_numeric, errors="coerce")
                    .fillna(0)
                )
            elif dtype == "date":
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors="coerce")
            elif dtype == "word":
                df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
            elif dtype == "review":
                df_cleaned[col] = df_cleaned[col].astype(str).apply(clean_review)

        return df_cleaned

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def clean_review(review):
    review = re.sub(r"[^a-zA-Z\s]", " ", review)
    review = review.lower()
    words = review.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)
