# models/recommendation.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def load_artist_database():
    # Load your artist database here
    # This is a placeholder
    return {
        "artist1": {"style": "Impressionism", "period": "19th century"},
        "artist2": {"style": "Cubism", "period": "20th century"},
        # Add more artists
    }


def recommend_artists(user_profile, artist_database):
    # Convert user profile and artist features to vectors
    user_vector = np.array(user_profile['preferences'])
    artist_vectors = np.array([list(artist.values()) for artist in artist_database.values()])

    # Calculate similarities
    similarities = cosine_similarity([user_vector], artist_vectors)[0]

    # Get top 5 recommendations
    top_indices = similarities.argsort()[-5:][::-1]
    recommended_artists = [list(artist_database.keys())[i] for i in top_indices]

    return recommended_artists

# Add more sophisticated recommendation algorithms here