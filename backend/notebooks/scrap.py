import pandas as pd 
import requests
from bs4 import BeautifulSoup
import time

with open("./animes_ids.txt", "r") as file:
    # Read the content of the file and split it into lines
    lines = file.read().split('\n')

url = "https://myanimelist.net/anime/"

df_animes = []

#if the for fails, save the data frame file 
for x in range(len(df)):
    info_dict = {
            "ID": "Unknown",
            "Type": "Unknown",
            "Episodes": "Unknown",
            "Status": "Unknown",
            "Aired": "Unknown",
            "Premiered": "Unknown",
            "Producers": "Unknown",
            "Licensors": "Unknown",
            "Studios": "Unknown",
            "Source": "Unknown",
            "Genres": "Unknown",
            "Duration": "Unknown",
            "Rating": "Unknown",
            "Favorites": "Unknown",
            "Title_Eng": "Unknown",
            "Title": "Unknown",
            "Score": "Unknown",
            "Ranked": "Unknown",
            "Members": "Unknown",
            "Favorites": "Unknown",
            "Popularity": "Unknown",
            "Synopsis":"Unknown"
        }

    
    id = df.iloc[x]['Number']
    
    if x % 80 == 0 and x > 0:
        time.sleep(200)

    if x % 100 == 0:
        print(x)

    response = requests.get(url+str(id))

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        info_dict = {
            "ID": "Unknown",
            "Type": "Unknown",
            "Episodes": "Unknown",
            "Status": "Unknown",
            "Aired": "Unknown",
            "Premiered": "Unknown",
            "Producers": "Unknown",
            "Licensors": "Unknown",
            "Studios": "Unknown",
            "Source": "Unknown",
            "Genres": "Unknown",
            "Duration": "Unknown",
            "Rating": "Unknown",
            "Favorites": "Unknown",
            "Title_Eng": "Unknown",
            "Title": "Unknown",
            "Score": "Unknown",
            "Ranked": "Unknown",
            "Members": "Unknown",
            "Favorites": "Unknown",
            "Popularity": "Unknown",
            "Synopsis":"Unknown"
        }
        info_dict["ID"] = id
        
        # Find all div elements with class "spaceit_pad"
        spaceit_pad_divs = soup.find_all('div', class_='spaceit_pad')

        # Loop through the "spaceit_pad" divs to extract the information
        for div in spaceit_pad_divs:
            non_html_text = ''.join([str(item) if item.name is None else '' for item in div.contents]).strip()
            span = div.find('span')
            if span:
                span_text = span.get_text()
                a = div.find('a')
                if "Type:" in span_text and a:
                    info_dict["Type"] = a.get_text()
                elif "Episodes:" in span_text:
                    info_dict["Episodes"] = non_html_text
                elif "Status:" in span_text:
                    info_dict["Status"] = non_html_text
                elif "Aired:" in span_text:
                    info_dict["Aired"] = non_html_text
                elif "Premiered:" in span_text and a:
                    info_dict["Premiered"] = a.get_text()
                elif "Producers:" in span_text and a:
                    info_dict["Producers"] = a.get_text()
                elif "Licensors:" in span_text and a:
                    info_dict["Licensors"] = a.get_text()
                elif "Studios:" in span_text and a:
                    info_dict["Studios"] = a.get_text()
                elif "Source:" in span_text:
                    info_dict["Source"] = non_html_text
                elif "Genres:" in span_text:
                    genres = div.find_all('a')
                    if genres:
                        info_dict["Genres"] = ", ".join(a.get_text() for a in genres)
                elif "Duration:" in span_text:
                    info_dict["Duration"] = non_html_text
                elif "Rating:" in span_text:
                    info_dict["Rating"] = non_html_text
                elif "Favorites:" in span_text:
                    info_dict["Favorites"] = non_html_text.replace(',', '')

        # Find the <p> element with itemprop="description"
        description_p = soup.find('p', itemprop='description')
        if description_p:
            # Split the text by lines
            lines = description_p.text.split('\n')
            # Check if the last line starts with "(Source:" and remove it
            if lines and lines[-1].strip().startswith("(Source:"):
                lines.pop()
            # Reconstruct the text without the last line
            description_p = '\n'.join(lines).strip()
            # Extract the cleaned text inside the <p> element
            info_dict["Synopsis"] = description_p


        score = soup.find('div', class_='fl-l score')
        if score:
            score = score.find('div', class_='score-label')
            info_dict["Score"] = score.text.strip()

        rank = soup.find('span', class_='numbers ranked')
        if rank:
            info_dict["Ranked"] = rank.strong.text.strip('#')

        popularity = soup.find('span', class_='numbers popularity')
        if popularity:
            info_dict["Popularity"] = popularity.strong.text.strip('#')

        members = soup.find('span', class_='numbers members')
        if members:
            info_dict["Members"] = members.strong.text.replace(',', '')


        title_name = soup.find('h1', class_='title-name h1_bold_none')
        if title_name:
            info_dict["Title"] = title_name.text


        title_english = soup.find('p', class_='title-english title-inherit')
        if title_english:
            info_dict["Title_Eng"] = title_english.text

        df_animes.append(info_dict)

    except Exception as e:
        print(f"Error occurred for ID {id}: {str(e)}")

        df_animes_df = pd.DataFrame(df_animes)
        df_animes_df.to_csv("anime_data.csv", index=False)

df_animes_df = pd.DataFrame(df_animes)
df_animes_df.to_csv("anime_data.csv", index=False)