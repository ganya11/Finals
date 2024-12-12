import altair as alt
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Movies Dataset", page_icon="🎥")

# Page title and description
st.title("🎥 Movies Dataset")
st.write(
    """
    This app visualizes data from [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
    It shows which movie genre performed best at the box office over the years. Use the widgets below to explore!
    """
)

# Load the data from a CSV file and cache it for performance
@st.cache_data
def load_data():
    """Load movies dataset."""
    return pd.read_csv("data/movies_genres_summary.csv")

# Load the dataset
df = load_data()

# Widgets for user interaction
# Multiselect widget for selecting genres
genres = st.multiselect(
    "Select Genres:",
    options=df["genre"].unique(),
    default=["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
)

# Slider widget for selecting a range of years
years = st.slider("Select Year Range:", 1986, 2016, (2000, 2016))

# Filter the dataframe based on user inputs
df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]

# Reshape the filtered data for visualization
df_reshaped = df_filtered.pivot_table(
    index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
).sort_values(by="year", ascending=False)

# Display the reshaped data as a table
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)

# Prepare data for chart visualization
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
)

# Create and display an Altair line chart
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year"),
        y=alt.Y("gross:Q", title="Gross Earnings ($)"),
        color=alt.Color("genre:N", title="Genre"),
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
