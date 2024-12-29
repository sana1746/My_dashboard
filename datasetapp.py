import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 15px;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stSidebar > div {
        background-color: #e6e6e6;
        padding: 10px;
        border-radius: 10px;
    }
    h1 {
        color: #333333;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
    }
    h2, h3 {
        color: #444444;
        margin-bottom: 20px;
    }
    .expander .stMarkdown {
        font-size: 14px;
        color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title of the dashboard
st.title("🌟 Interactive Data Dashboard 🌟")

# File uploader widget
uploaded_file = st.file_uploader("📂 Please upload your CSV file here", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    st.success("✔️ File uploaded successfully!")

    # Dataset Preview
    st.subheader("📊 Dataset Overview")
    with st.expander("👀 Preview Dataset"):
        st.write(data.head())

    # Summary Statistics
    st.subheader("📈 Summary Statistics")
    with st.expander("📋 View Summary"):
        st.write(data.describe())

    # Visualization options
    st.subheader("🎨 Select Columns of Your Choice for Visualization")
    column_to_visualize = st.selectbox("🎯 Select a column for visualization", data.columns)
    columns_to_visualize = st.multiselect("📚 Select multiple columns for analysis", data.columns)

    if column_to_visualize:
        st.subheader("📊 Visualizations")

        # Dynamic plot selection
        plot_type = st.radio("📍 Choose plot type", ["Line Chart", "Bar Chart", "Box Plot", "Scatter Plot"])

        if plot_type == "Line Chart" and data[column_to_visualize].dtype in ['int64', 'float64']:
            st.line_chart(data[column_to_visualize])

        elif plot_type == "Bar Chart" and data[column_to_visualize].dtype == 'object':
            chart_data = data[column_to_visualize].value_counts()
            fig = px.bar(chart_data, x=chart_data.index, y=chart_data.values, labels={'x': column_to_visualize, 'y': 'Count'})
            st.plotly_chart(fig)

        elif plot_type == "Box Plot" and data[column_to_visualize].dtype in ['int64', 'float64']:
            fig = px.box(data, y=column_to_visualize, points="all")
            st.plotly_chart(fig)

        elif plot_type == "Scatter Plot" and data[column_to_visualize].dtype in ['int64', 'float64']:
            fig = px.scatter(data, x=column_to_visualize, y=data.columns[0])
            st.plotly_chart(fig)

    if columns_to_visualize:
        st.subheader("📊 Histogram for Selected Columns")
        for col in columns_to_visualize:
            if data[col].dtype in ['int64', 'float64']:
                fig = px.histogram(data, x=col, marginal="box", nbins=30, title=f"Distribution of {col}")
                st.plotly_chart(fig)

    # Sidebar filters
    st.sidebar.header("🛠️ Filter Options")
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns

    if len(numeric_columns) > 0:
        st.sidebar.subheader("🔍 Filter by Numeric Column")
        for col in numeric_columns:
            min_val, max_val = st.sidebar.slider(
                f"Range for {col}",
                float(data[col].min()),
                float(data[col].max()),
                (float(data[col].min()), float(data[col].max()))
            )
            data = data[(data[col] >= min_val) & (data[col] <= max_val)]

    # Filtered Data Display
    st.subheader("📄 Filtered Dataset")
    st.write(data)

    # Download Dataset
    st.subheader("💾 Download Processed Dataset")
    st.download_button(
        label="⬇️ Download CSV",
        data=data.to_csv(index=False).encode('utf-8'),
        file_name="processed_data.csv",
        mime="text/csv"
    )
