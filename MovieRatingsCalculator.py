import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from imdb import IMDb
import requests
import sys
import os

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


DEFAULT_API_KEY = "f8e3a86ccbc7360ff7b4d84c56c19edc"

def get_imdb_rating(movie_title):
    ia = IMDb()
    movies = ia.search_movie(movie_title)
    if movies:
        movie = ia.get_movie(movies[0].getID())
        return movie.data['rating']
    return None

def get_tmdb_rating(movie_title, api_key):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': api_key,
        'query': movie_title,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'results' in data and data['results']:
        return data['results'][0].get('vote_average')

    return None

def get_average_rating(imdb_rating, tmdb_rating):
    if imdb_rating is not None and tmdb_rating is not None:
        return (float(imdb_rating) + float(tmdb_rating)) / 2
    return None

def calculate_ratings(event=None):
    movie_title = entry_movie.get()

    if not movie_title:
        messagebox.showwarning("Warning", "Please enter a movie title.")
        return

    imdb_rating = get_imdb_rating(movie_title)
    tmdb_rating = get_tmdb_rating(movie_title, DEFAULT_API_KEY)
    average_rating = get_average_rating(imdb_rating, tmdb_rating)

    # Format ratings to display one decimal place, handling None values
    imdb_rating_formatted = round(float(imdb_rating), 1) if imdb_rating is not None else "N/A"
    tmdb_rating_formatted = round(float(tmdb_rating), 1) if tmdb_rating is not None else "N/A"
    average_rating_formatted = round(float(average_rating), 1) if average_rating is not None else "N/A"

    result_text.set(f"IMDb rating: {imdb_rating_formatted}\nTMDb rating: {tmdb_rating_formatted}\nAverage rating: {average_rating_formatted}")

# Main window
root = tk.Tk()
root.title("Movie Rating Calculator")

# Size of window
window_width = 800  # Increase the desired width by 600 pixels
window_height = 600  # Increase the desired height by 600 pixels
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Background color
root.configure(bg='black')

label_movie = ttk.Label(root, text="Movie Title:", font=("Helvetica", 16), background='black', foreground='white')
label_movie.grid(row=0, column=0, pady=15)

entry_movie = ttk.Entry(root, width=30, justify="center", font=("Helvetica", 16), background='black', foreground='black')  # Set a fixed width
entry_movie.grid(row=1, column=0, pady=15, padx=20)

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 16), background='white', foreground='black')

button_calculate = ttk.Button(root, text="Calculate Ratings", command=calculate_ratings, style='TButton')
button_calculate.grid(row=2, column=0, pady=25)

result_text = tk.StringVar()
label_result = ttk.Label(root, textvariable=result_text, font=("Helvetica", 16), background='black', foreground='white')
label_result.grid(row=3, column=0, pady=15)

# Row and column weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# Binding Enter key to "calculate" button
entry_movie.bind("<Return>", calculate_ratings)

# Start the GUI main loop
root.mainloop()