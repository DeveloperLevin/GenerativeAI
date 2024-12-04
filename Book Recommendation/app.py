import pandas as pd
import numpy as np
import requests
import faiss

dataset = pd.read_csv('dataset/books.csv')

def textual_representation(row):
    """Iterates through all the rows in the dataset and only extracts the necessary information and store it in a variable
    as String named textual_representation
    
    input: row -> parameter, datatype ->  DataFrame Object
    output: return textual_representation -> String 
    """
    textual_representation = f"""
    Title: {row['title']}
    Authors: {row['authors']}
    Description: {row['description']}
    Categories: {row['categories']}
    Publishing Year: {row['published_year']}
    Average Rating: {row['average_rating']}
    Number of pages: {row['num_pages']}"""

    return textual_representation

def model_result(query):
    """The function takes one parameter named query and makes a request to ollama api for the llama2 model to generate 
    embedding for the user prompt, the embedding is then used to retrieve the the 5 nearest vectors using Euclidean distance from the faiss 
    vector store
    
    Input: (query) 1 parameter -> String
    Output: (best_matches) -> np Object
    """
    user_input_response = requests.post('http://localhost:11434/api/embeddings',
                        json = {
                            'model': 'llama2',
                            'prompt': query
                        })
    user_input_embedding = np.array([user_input_response.json()['embedding']], dtype='float32')

    D, I = index.search(user_input_embedding, 3)

    best_matches = np.array(dataset['textual_representation'])[I.flatten()]

    return best_matches


def prompt_generator(title, author, description, categories, published_year, average_rating, num_pages):
    """ Forms a String template with the user input

        input: 7 parameters -> String
        output: one return value -> String 
    """
    textual_representation = f"""
    Title: {title}
    Authors: {author}
    Description: {description}
    Categories: {categories}
    Publishing Year: {published_year}
    Average Rating: {average_rating}
    Number of pages: {num_pages}"""

    return textual_representation

system_not_available = False

dataset['textual_representation'] = dataset.apply(textual_representation, axis=1)

# Load the pre-saved FAISS index
index_file = 'index'  # Update this to your actual file name
try:
    index = faiss.read_index(index_file)
    print(f"FAISS index loaded from {index_file}.")
except Exception as e:
    print(f"Error loading FAISS index: {e}")
    exit()

while not system_not_available:
    user_input = input("Welcome to Book Recommendation Engine!\n Fill out these details so we can curate some good recommendation for you\n\n" +
        "Type 'X' to exit the Engine. Press ANY other key to 'Start'\n\n")

    # Base Condition to exit the while loop
    if user_input.lower() == 'x':
        system_not_available = True
        exit()

    # user input data required for search operation
    input_title = input("What is title of the book: ")
    input_author = input("Who is the author of the book: ")
    input_description = input("Whats the description of the book: ")
    input_category = input("What genre is it: ")
    input_publishing_year = input("Which year was it published: ")
    input_rating = input("What is the user rating (5 being the highest): ")
    input_num_pages = input("What is the total amount of pages you want: ")

    prompt_template = prompt_generator(input_title, input_author, input_description, input_category, input_publishing_year, input_rating, input_num_pages)

    try:
        results = model_result(prompt_template)
    except Exception as e:
        print(e)
        print("Try Again")
        system_not_available = True
        exit()
    else:
        for result in results:
            print(result + "\n")