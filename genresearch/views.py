import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import xlrd
from matplotlib import pyplot as plt
from io import BytesIO
import base64

def genresearch(request):
    if 'genre' in request.GET:
        # Read the Excel file
        excel_file = 'movies.xls'
        
        # Read all sheets into a dictionary of DataFrames
        movies_dict = pd.read_excel(excel_file, sheet_name=['1900s', '2000s', '2010s'])
        
        # Combine the DataFrames into a single DataFrame
        combined_movies = pd.concat([movies_dict['1900s'], movies_dict['2000s'], movies_dict['2010s']], ignore_index=True)
        
        # Create a new DataFrame with selected columns
        selected_columns_df = combined_movies[['Title', 'Year', 'Genres', 'Country', 'Language', 'Duration', 'IMDBScore']]

        # Get genre input from the user
        genre_input = request.GET.get('genre', '')  # Use GET parameter for genre input

        # Filter movies based on genre input
        if genre_input:
            filtered_movies = selected_columns_df[selected_columns_df['Genres'].str.contains(genre_input, case=False, na=False)]
        else:
            filtered_movies = selected_columns_df

        # Sort the filtered movies by 'IMDBScore'
        sorted_filtered_movies = filtered_movies.sort_values(by=['IMDBScore'], ascending=False)

        top_100_movies = sorted_filtered_movies.head(100)

        # Store the results in the session
        request.session['filtered_movies'] = top_100_movies.to_dict(orient='records')
        # orient store the dataframe in dictionary form.
        request.session['genre_input'] = genre_input

        return redirect('showmovies')
    
    return render(request, 'genresearch.html')

def showmovies(request):
    # Retrieve the filtered movies from the session
    filtered_movies = request.session.get('filtered_movies', [])  # we have taken empty array to store the dictionary in array form.
    genre_input = request.session.get('genre_input', '')

    # Pass the data to the template
    context = {
        'movies': filtered_movies,
        'genre_input': genre_input,
    }
    return render(request, 'show_movies.html', context)

def moviesearch(request):
    if 'title' in request.GET:
        # Read the Excel file
        excel_file = 'movies.xls'
        # Read all sheets into a dictionary of DataFrames
        movies_dict = pd.read_excel(excel_file, sheet_name=['1900s', '2000s', '2010s'])
        
        # Combine the DataFrames into a single DataFrame
        combined_movies = pd.concat([movies_dict['1900s'], movies_dict['2000s'], movies_dict['2010s']], ignore_index=True)
         # Create a new DataFrame with selected columns
        selected_columns_df = combined_movies[['Title', 'Year', 'Genres', 'Country', 'Language', 'Duration', 'IMDBScore', 'Facebooklikes', 'ReviewsbyUsers']]
         # Get genre input from the user
        title_input = request.GET.get('title', '')  # Use GET parameter for genre input
         # Filter movies based on genre input
        if title_input:
            filtered_movies = selected_columns_df[selected_columns_df['Title'].str.contains(title_input, case=False, na=False)]
        else:
            filtered_movies = selected_columns_df
        # Store the results in the session
        request.session['filtered_movies'] = filtered_movies.to_dict(orient='records')
        request.session['title_input'] = title_input
        return redirect('titleshow')
    return render(request, 'search_movie.html')

def titleshow(request):
     # Retrieve the filtered movies from the session
    filtered_movies = request.session.get('filtered_movies', [])
    genre_input = request.session.get('genre_input', '')
     # Convert the list of dictionaries back to a DataFrame
    df = pd.DataFrame(filtered_movies)

    # Generate a plot (e.g., IMDB Scores vs. Duration)
    plt.figure(figsize=(7, 4))
    # Plot Facebook likes
    plt.scatter(df['Facebooklikes'], df['IMDBScore'], color='blue', alpha=0.5, label='Facebook Likes')

# Plot Reviews by Users
    plt.scatter(df['ReviewsbyUsers'], df['IMDBScore'], color='red', alpha=0.5, label='Reviews by Users')
    # plt.scatter(df['Facebooklikes'], df['ReviewsbyUsers'], df['IMDBScore'], alpha=0.5)
    # alpha 0.5 is for opacity.
    # plt.title('IMDB Score vs. Facebooklikes')
    plt.xlabel('Facebooklikes')
    plt.ylabel('IMDB Score')
    
    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encode the image to base64 to pass to the template
    graph = base64.b64encode(image_png).decode('utf-8')
    # Pass the data to the template
    context = {
        'movies': filtered_movies,
        'genre_input': genre_input,
        'graph': graph,
    }
    return render(request, 'search_movie.html', context)


