import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Load Model and Data ---
# This part runs once when the module is imported, making the app faster.

try:
    # Load the movies dataset from the CSV file.
    df = pd.read_csv('movies.csv')
    
    # Load the pre-trained model specified for the assignment.
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create vector embeddings for all movie plots.
    embeddings = model.encode(df['plot'].tolist(), show_progress_bar=False)
    
except FileNotFoundError:
    print("Error: 'movies.csv' not found. Ensure the file is in the same directory.")
    df = None
    embeddings = None

# --- 2. The Search Function ---

def search_movies(query: str, top_n: int = 5):
    """
    Finds the top_n movies most similar to a given query.

    Args:
        query (str): The search query from the user.
        top_n (int): The number of top results to return.

    Returns:
        pandas.DataFrame: A DataFrame with the top matching movies,
                          including a 'similarity' score, as required
                          by the unit tests.
    """
    if df is None:
        # Return an empty DataFrame if data loading failed.
        return pd.DataFrame()

    # 1. Encode the search query into a vector.
    query_embedding = model.encode([query])

    # 2. Calculate cosine similarity between the query and all movie plots.
    sim_scores = cosine_similarity(query_embedding, embeddings)[0]

    # 3. Get the indices of the top_n most similar movies.
    top_indices = np.argsort(sim_scores)[-top_n:][::-1]

    # 4. Create a results DataFrame from the original data.
    results_df = df.iloc[top_indices].copy()

    # 5. Add the similarity scores to the results DataFrame.
    results_df['similarity'] = [sim_scores[i] for i in top_indices]

    return results_df