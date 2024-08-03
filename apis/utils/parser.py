import xml.etree.ElementTree as ET
import csv
import pandas as pd

def parse_xml_user(username):
    # Should have a method to check if the username already has a csv file
    xml_data = pd.DataFrame()
    try:
        xml_data = pd.read_xml(f"{username}.xml")
    except:
        return Exception("Could not find the username csv file.")

    # Assign some random ID, for now, it doesn't have to be unique
    xml_data['user_id'] = 786
    df = xml_data[["user_id", "series_animedb_id", "my_score"]]
    df.columns = ["user_id", "anime_id", "rating"]

    df.to_csv(f"{username}.csv", index=False)
    return True