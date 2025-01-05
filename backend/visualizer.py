import plotly.express as px
import pandas as pd
from fastapi import HTTPException

def generate_chart(df, label, connection):
    try:
        df = pd.DataFrame(df)

        if df[connection].dtype == "object":
            grouped_data = (
                df.groupby(label)[connection]
                .nunique()
                .reset_index()
            )
        else:
            grouped_data = (
                df.groupby(label)[connection]
                .sum()
                .reset_index()
            )
        
        grouped_data['connection_name'] = df[connection].astype(str)
        
        fig = px.bar(
            grouped_data,
            x=label,
            y=connection,
            title=f"{connection} by {label}",
            text=grouped_data['connection_name']
        )

        return fig.to_html(full_html=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
