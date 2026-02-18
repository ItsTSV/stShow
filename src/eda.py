import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load the dataset
df = pd.read_csv("data/pinvgin.csv")
df = df.dropna()

# Dynamically update the dataset based on sidebar filters
st.sidebar.header("Filter Settings")
selected_islands = st.sidebar.multiselect(
    "Select Island(s):", options=df["island"].unique(), default=df["island"].unique()
)
selected_sex = st.sidebar.multiselect(
    "Select Sex:", options=df["sex"].unique(), default=df["sex"].unique()
)
df_filtered = df[(df["island"].isin(selected_islands)) & (df["sex"].isin(selected_sex))]

# Main EDA content
st.title("Exploratory Data Analysis")
st.markdown("""
The dataset we are working with is called **"Palmer Penguins"**.

It’s the modern alternative to the classic Iris dataset. It contains data for **344 penguins** from **3 species** 
(Adélie, Chinstrap, and Gentoo) observed on **3 islands** in the Palmer Archipelago, Antarctica. 

It's a perfect playground for EDA because it combines:
* **Numeric data:** Bill length, flipper length, and body mass.
* **Categorical data:** Species, island, and sex.
""")

# Use components to perform EDA
st.subheader("Dataset Overview")
with st.expander("Show raw data", expanded=True):
    st.dataframe(df_filtered)
with st.expander("Show summary statistics"):
    st.write(df_filtered.describe())
st.divider()

# Streamlit does have some built-in charts, but it's better to use Matplotlib/Seaborn
c1, c2 = st.columns(2, gap="large")
with c1:
    st.subheader("Categorical Features")
    t1, t2, t3 = st.tabs(["Species", "Islands", "Sexes"])
    with t1:
        fig_c, ax_c = plt.subplots()
        sns.countplot(x=df_filtered["species"], palette="Set2")
        sns.despine(left=True, bottom=True)
        ax_c.set_xlabel("")
        ax_c.set_ylabel("Count")
        st.pyplot(fig_c)
    with t2:
        fig_c, ax_c = plt.subplots()
        sns.countplot(x=df_filtered["island"], palette="Set2")
        sns.despine(left=True, bottom=True)
        ax_c.set_xlabel("")
        ax_c.set_ylabel("Count")
        plt.tight_layout()
        st.pyplot(fig_c)
    with t3:
        fig_c, ax_c = plt.subplots()
        sns.countplot(x=df_filtered["sex"], palette="Set2")
        sns.despine(left=True, bottom=True)
        ax_c.set_xlabel("")
        ax_c.set_ylabel("Count")
        plt.tight_layout()
        st.pyplot(fig_c)
with c2:
    st.subheader("Numeric Features")
    t1, t2, t3 = st.tabs(["Bill Length", "Flipper Length", "Body Mass"])
    with t1:
        fig_n, _ = plt.subplots()
        sns.histplot(df_filtered["bill_length_mm"], kde=True, color="#66c2a5")
        sns.despine(left=True, bottom=True)
        st.pyplot(fig_n)
    with t2:
        fig_n, _ = plt.subplots()
        sns.histplot(df_filtered["flipper_length_mm"], kde=True, color="#66c2a5")
        sns.despine(left=True, bottom=True)
        st.pyplot(fig_n)
    with t3:
        fig_n, _ = plt.subplots()
        sns.histplot(df_filtered["body_mass_g"], kde=True, color="#66c2a5")
        sns.despine(left=True, bottom=True)
        st.pyplot(fig_n)
st.divider()

# Correlation scatter plot
c1, c2 = st.columns([2, 1], gap="large")
with c1:
    st.subheader("Correlation Analysis")
    fig_corr, ax_corr = plt.subplots()
    sns.scatterplot(
        x=df_filtered["bill_length_mm"],
        y=df_filtered["body_mass_g"],
        hue=df_filtered["species"],
        palette="Set2",
        ax=ax_corr,
    )
    sns.despine(left=True, bottom=True)
    ax_corr.set_xlabel("Bill Length (mm)")
    ax_corr.set_ylabel("Body Mass (g)")
    ax_corr.legend(title="Species")
    st.pyplot(fig_corr)
with c2:
    st.subheader("Correlation Matrix")
    corr = df_filtered[
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    ].corr()
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="YlGnBu", ax=ax_corr, fmt=".2f", cbar=False)
    plt.xticks(rotation=45)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig_corr)
st.divider()

# Distribution box plot
st.subheader("Distribution by Species")
c1, c2 = st.columns(2, gap="large")
with c1:
    fig, ax = plt.subplots()
    sns.boxplot(data=df_filtered, x="species", y="body_mass_g", palette="Set2")
    sns.despine(left=True, bottom=True)
    ax.set_xlabel("")
    ax.set_ylabel("Body Mass (g)")
    st.pyplot(fig)

with c2:
    fig, ax = plt.subplots()
    sns.boxplot(data=df_filtered, x="species", y="flipper_length_mm", palette="Set2")
    sns.despine(left=True, bottom=True)
    ax.set_xlabel("")
    ax.set_ylabel("Flipper Length (mm)")
    st.pyplot(fig)
