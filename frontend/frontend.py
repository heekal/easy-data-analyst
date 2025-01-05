import streamlit as st
import pandas as pd
import requests
import base64

# Backend URL
BACKEND_URL = "http://localhost:8000"

def call_cleaning_service(data, column_types):
    response = requests.post(
        f"{BACKEND_URL}/clean-data",
        json={"data": data, "column_types": column_types}
    )
    response.raise_for_status()
    return response.json()["cleaned_data"]

def call_chart_service(data, label, connection):
    response = requests.post(
        f"{BACKEND_URL}/generate-chart",
        json={"data": data, "label": label, "connection": connection}
    )
    response.raise_for_status()
    return response.json()["chart_html"]

def call_wordcloud_service(texts):
    response = requests.post(
        f"{BACKEND_URL}/generate-wordcloud",
        json={"texts": texts}
    )
    response.raise_for_status()
    return response.json()["img"]

def main():
    with st.sidebar:
        st.header("Upload Your CSV File")
        file = st.file_uploader("Upload Here:", type="csv")

    if file is None:
        st.title("Please upload your CSV file!")
        return

    try:
        df = pd.read_csv(file).drop_duplicates().dropna()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    columns = df.columns.tolist()

    selected_columns = st.sidebar.pills(
        label="Core Datas:",
        options=df.columns,
        selection_mode="multi"
    )

    if not selected_columns:
        st.title("Please select columns to analyze!")
        return

    sorted_columns = selected_columns + [col for col in columns if col not in selected_columns]
    
    st.title(f"{file.name[:-4]} Dashboard")

    tabs = st.tabs(["Settings"] + selected_columns)

    column_types = {}
    column_connections = {}

    with tabs[0]:
        st.subheader("Your Datas: ")
        st.dataframe(df)

        st.subheader("Column Configuration:")
        for col in sorted_columns:
            with st.container(border=True):
                st.markdown(f"### {col}")
                column_types[col] = st.segmented_control(
                    label = f"Select type for {col}:",
                    options=["word", "review", "rating", "number", "date"],
                    selection_mode="single",
                    key=f"type-{col}"
                )
                if col in selected_columns:
                    column_connections[col] = st.multiselect(
                        f"Connect {col} to other columns:",
                        options=columns,
                        key=f"conn-{col}",
                    )


    df_cleaned = call_cleaning_service(df.to_dict(orient='list'), column_types)

    for col, tab in zip(selected_columns, tabs[1:]):
        with tab:
            type = column_types[col]
            connections = column_connections[col]

            st.subheader(f"Analysis for {col}")

            if type == "review":
                text = " ".join(df_cleaned[col])
                img_base64 = call_wordcloud_service(text)
                if img_base64:
                    img_data = base64.b64decode(img_base64)
                    st.image(img_data, use_container_width=True)

            
            if  isinstance(df_cleaned[col][1], str) :
                df_metric = pd.DataFrame(df_cleaned)      
                total, sum, mean = st.columns(3)
                total.container(border=True).metric(f"Total {col} Data", df_metric[col].nunique())
                sum.container(border=True).metric(f"Most Frequent {col}", df_metric[col].value_counts().idxmax(), f"{int(df_metric[col].value_counts().max())} Times")
                mean.container(border=True).metric(f"Average {col} Appears", df_metric[col].value_counts().mean())
            else:
                df_metric = pd.DataFrame(df_cleaned)  
                total, sum, mean = st.columns(3)
                total.container(border=True).metric(f"Total {col} Data", df_metric[col].count())
                sum.container(border=True).metric(f"Sum of {col}", df_metric[col].sum())
                mean.container(border=True).metric(f"Average {col}", df_metric[col].mean())
            
                

            for connection in connections:
                chart_html = call_chart_service(
                    df_cleaned,
                    col,
                    connection,
                )
                if chart_html:
                    st.components.v1.html(chart_html, height=500, scrolling=True)


if __name__ == "__main__":
    main()
