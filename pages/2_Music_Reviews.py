import streamlit as st
import pandas as pd
import unicodedata

# Load the CSV file with the correct encoding
df = pd.read_csv("contemp_music_reviews.csv", encoding='utf-8')

# Drop rows with missing values
df.dropna(inplace=True)

# Normalize artist names and titles
df['Artist'] = df['Artist'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
df['Title'] = df['Title'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))

# Title and description
st.title("Album Reviews")
st.write("To view the analysis for an album, please select the artist and album from the dropboxes below.")

# Select Artist
st.header('Select Artist')
artist_input = st.selectbox('Search Artist', df['Artist'].unique())

# Filter the dataframe based on the artist input
filtered_artists = df[df['Artist'].str.lower().str.contains(artist_input.lower(), case=False)]

# Select Album
st.header('Select Album')
album_selected = st.selectbox('Album', filtered_artists['Title'].unique())

# Display all reviews for the selected artist and album
if album_selected:
    selected_reviews = filtered_artists[filtered_artists['Title'] == album_selected]
    st.subheader('All Reviews')
    for index, review_row in selected_reviews.iterrows():
        review_text = review_row['Review']
        analysis = review_row['Analysis']  # Corrected column name to 'Analysis'
        # Set the color based on sentiment analysis
        if analysis.lower() == 'positive comment':
            color = 'green'
        elif analysis.lower() == 'negative comment':
            color = 'red'
        else:
            color = 'black'  # Default color if sentiment is not specified
        # Create curved textbox with dynamically assigned color
        st.markdown(f"<div style='border: 1px solid {color}; border-radius: 5px; padding: 10px; margin-bottom: 10px;'>{review_text}<br>Sentiment Analysis: {analysis}</div>", unsafe_allow_html=True)
    
    # Calculate and display average rating
    average_rating = selected_reviews['Adjusted_Review'].mean()
    st.subheader('Average Rating')
    if 0 <= average_rating <= 2:
        st.write(f"<span style='color:red;'>{average_rating:.2f}</span>", unsafe_allow_html=True)
    elif 2 < average_rating <= 4:
        st.write(f"<span style='color:orange;'>{average_rating:.2f}</span>", unsafe_allow_html=True)
    elif average_rating > 4:
        st.write(f"<span style='color:green;'>{average_rating:.2f}</span>", unsafe_allow_html=True)

    # Prepare data for the bar chart
    ratings_distribution = selected_reviews['Adjusted_Review'].apply(lambda x: int(x))
    rating_counts = ratings_distribution.value_counts().sort_index()
    all_bins = pd.Series(0, index=range(6))
    all_bins.update(rating_counts)

    # Plot the bar chart using st.bar_chart()
    st.subheader('Rating Distribution')
    st.bar_chart(all_bins)