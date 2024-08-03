```java
- /apis
        |_ app.py               // API, contains routes to everything
        |_ colab.py             // ColaborativeRecommender class model
        |_ denoising.py         // DenoisingAutoEncoder class model
        |_ model_categorical.py // Content_Categorical class model
        |_ model_content.py     // ContentBasedRecommender class model
        |_ model_genres.py      // Content_Genre class model
        |_ model_hybrid.py      // HybridRecommender class model
        |_ model_numerical.py   // Content_Numerical class model
        |_ model_st.py          // Content_Meta class model
        |_ model_studio.py      // Content_Studio class model
        |_ /utils // Utility functions not necessarely used in the API
                |_ conversion.py        // Turns .keras model into .h5
                |_ test.py              // Test template to test an API
                |_ parser.py // Future implementation where people can upload their XML files instead of scrapiing their profiles if their account is private.
        |_ /data
                |_ 10k.csv: // Id's of shows with more than 10k members.
                |_ anime_genres.csv: // File containing the id's and a one-hot encoding of their genres.
                |_ anime_titles.csv: // Id's and their respective titles.
                |_ anime_with_synopsis.csv: // Id's, Title, Score, Genres cleaned but separated by commas, and synopsis.
                |_ anime.csv: // idk
                |_ data_anime_almclean.csv: // idk
                |_ data_anime_clean.csv: // Main data for the page
                |_ data4filter.csv: // Used for filtering data
                |_ data4filter2.csv
                |_ Studios.csv: // File containing the id's and a one-hot encoding of their studios.
        |_ /models
                |_ 7hours.keras: // Keras wrong format
                |_ autoencoder.h5: // Denoising Auto-encoder model
                |_ model.h5: // Denoising FCN model
                |_ model_warp_1.pkl: // Collab filtering (diego)
                |_ model_pr_100_...: // Collab filtering (diego)
                |_ dataset_save.pkl: // Collab filtering (diego)


- /interactive: // Currently testing the interactive profile

- /notebooks (should be moved to another space)
        |_ /scraping: // Contains the csv from 1970-fall to 2024-winter (need data cleaning)
        // There are notebooks testing the models and some filtering or scraping, should be moved to another space as documentation.

- /public
        |_ /build // Svelte stuff, do not touch lol
        |_ /download // <id>.jpg: its the background image for each anime
            |_ /profiles // <id>.jpg: mal scrapped poster for each anime
        |_ /fonts
            |_ Lato.ttf family font
        |_ /icons
            |_ <number from 1 to 10>.png // Icon for Top-x ranked anime in the top 10 recommendations
            |_ anilist.png & mal.png // Logos
            |_ ThumbsDown.png & ThumbsUp.png // Icons for the feedback model
        |_ /images
            |_ <name>.jpg // Background images from the main page slideshow
        |_ /users
            |_ <user>.csv // Scrapped users from mal

- /src
        |_ /routes
                |_ About.svelte // Recommendations Page
                |_ Home.svelte // Main Page 
                |_ Credits.svelte // tbd
                |_ FAQ.svelte // tbd
                |_ Stats.svelte // tbd
        |_ api.js // Functions for API calls to apply filters on data
        |_ App.svelte // Main page and Router, connects to /, /about, /faq, /credits
        |_ main.js // Svelte initializator file for App.svelte, props and export default app
        |_ store.js // Store, contains the suscribable variables to manage across routes


```