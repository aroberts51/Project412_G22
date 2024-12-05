import requests
import psycopg2
import csv
from datetime import datetime, timezone


# Step 1: Set up the Twitch/IGDB API credentials
client_id = 'c41lif1fph7aclvubfk0bgih6wrt98'
access_token = 'uf4d835hqbnd3ldsl0p7nu1bycfb1f'
api_url = 'https://api.igdb.com/v4/games/'
api_url2 = 'https://api.igdb.com/v4/companies'

# Get Access Token
url = 'https://id.twitch.tv/oauth2/token'
data = {
    'client_id': client_id,
    'client_secret': access_token,
    'grant_type': 'client_credentials'
}
response = requests.post(url, data=data)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    print(f'Access Token: {access_token}')
else:
    print(f'Failed to get access token: {response.status_code} - {response.text}')
    exit()

# Step 2: Set up PostgreSQL connection
conn = psycopg2.connect(
    dbname='412Proj_D1', #name of database
    user='igdb_user', #name of user you will use to access database
    password='0315', #password for postgre
    host='localhost', #dont change (for local machine)
    port='5432' #default port number for psql
)
cursor = conn.cursor()

# Step 3: Define the data request to the IGDB API
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}
# Updated query to include summary and cover URL
data = """
fields id, name, genres.name, first_release_date, platforms.name, involved_companies.company.name, hypes, rating, summary, cover.url;
sort hypes desc;
limit 500;
"""
response = requests.post(api_url, headers=headers, data=data)

if response.status_code == 200:
    print("Raw response content:", response.text)  # Print the raw response to see what you are receiving
    games = response.json()  # Parse the response as JSON

    # Step 4: Prepare CSV files
    with open('Game.csv', mode='w', newline='', encoding='utf-8') as game_file, \
         open('Genre.csv', mode='w', newline='', encoding='utf-8') as genre_file, \
         open('Publisher.csv', mode='w', newline='', encoding='utf-8') as publishers_file, \
         open('Platform.csv', mode='w', newline='', encoding='utf-8') as platform_file:

        # Create CSV writers
        game_writer = csv.writer(game_file, quoting=csv.QUOTE_NONE, escapechar='\\')  # Quote fields with commas
        genre_writer = csv.writer(genre_file)
        platform_writer = csv.writer(platform_file)
        publishers_writer = csv.writer(publishers_file)

        # Write CSV headers
        game_writer.writerow(['GameID', 'GameName', 'ReleaseDate', 'Rating', 'Summary', 'CoverURL', 'PublisherID'])
        genre_writer.writerow(['GenreID', 'GenreName'])
        platform_writer.writerow(['PlatformID', 'PlatformName'])
        publishers_writer.writerow(['PublisherID', 'PublisherName'])

        genre_set = set()  # To avoid duplicates in genres
        platform_set = set()  # To avoid duplicates in platforms
        publisher_set = set() # To avoid duplicates in publishers

        for game in games:
            # Insert into Game CSV
            game_id = game.get('id')
            game_name = game.get('name')
            release_date_unix = game.get('first_release_date')
            rating = (game.get('rating', 0)) / 10
            summary = game.get('summary', '').replace('\n', ' ')#.replace(',', ';')  # Replace commas with semicolons
            
            summary = "'" + summary + "'"
            cover_url = game.get('cover', {}).get('url')  # Get cover URL if it exists

            if release_date_unix:
                # Use timezone-aware datetime object
                release_date = datetime.fromtimestamp(release_date_unix, tz=timezone.utc).strftime('%Y-%m-%d')
            else:
                release_date = 'NULL' 

            # Default publisher ID (to be replaced with the actual publisher)
            publisher_id = 1

            game_writer.writerow([game_id, game_name, release_date, rating, summary, cover_url, publisher_id])

            # Process genres
            if 'genres' in game:
                for genre in game['genres']:
                    genre_name = genre.get('name')
                    if genre_name and genre_name not in genre_set:
                        genre_set.add(genre_name)
                        genre_writer.writerow([len(genre_set), genre_name])

            # Process platforms
            if 'platforms' in game:
                for platform in game['platforms']:
                    platform_name = platform.get('name')
                    if platform_name and platform_name not in platform_set:
                        platform_set.add(platform_name)
                        platform_writer.writerow([len(platform_set), platform_name])

            # Process involved companies (publishers and developers)
            if 'involved_companies' in game:
                for involved_company in game['involved_companies']:
                    company_name = involved_company.get('company', {}).get('name')
                    if company_name:
                        # Add the company name to your database or handle it as needed
                        publisher_set.add(company_name)
                        publishers_writer.writerow([len(publisher_set), company_name])
                        #print(f"Company involved: {company_name}")


    print("CSV files created successfully.")

    # Step 5: Insert data into PostgreSQL database
    # Load and insert Game data
    with open('Game.csv', mode='r', encoding='utf-8') as game_file:
        next(game_file)  # Skip header
        cursor.copy_from(game_file, 'game', sep=',', columns=('gameid', 'gamename', 'releasedate', 'rating', 'summary' , 'coverurl', 'publisherid'))

    # Commit changes to the database
    conn.commit()
    print("Data inserted into PostgreSQL tables successfully.")

else:
    print(f"Failed to fetch game data: {response.status_code} - {response.text}")

# Close the cursor and connection
cursor.close()
conn.close()


try:
    conn = psycopg2.connect(
    dbname='412Proj_D1',
    user='igdb_user',
    password='0315',
    host='localhost',
    port='5432'
    )
    cursor = conn.cursor()
    # Load and insert Genre data
    with open('Genre.csv', mode='r', encoding='utf-8') as genre_file:
        next(genre_file)  # Skip header
        cursor.copy_from(genre_file, 'genres', sep=',', columns=('genreid', 'genrename'))
except psycopg2.Error as e:
    conn.rollback()  # Rollback any changes made during this copy operation
    # Close the cursor and connection
    cursor.close()
    conn.close()

try:
    conn = psycopg2.connect(
    dbname='412Proj_D1',
    user='igdb_user',
    password='0315',
    host='localhost',
    port='5432'
    )
    cursor = conn.cursor()
    # Load and insert Platform data
    with open('Platform.csv', mode='r', encoding='utf-8') as platform_file:
        next(platform_file)  # Skip header
        cursor.copy_from(platform_file, 'platforms', sep=',', columns=('platformid', 'platformname'))
except psycopg2.Error as e:
    conn.rollback()  # Rollback any changes made during this copy operation
    # Close the cursor and connection
    cursor.close()
    conn.close()

try:
    conn = psycopg2.connect(
    dbname='412Proj_D1',
    user='igdb_user',
    password='0315',
    host='localhost',
    port='5432'
    )
    cursor = conn.cursor()
    # Load and insert publisher data
    with open('Publisher.csv', mode='r', encoding='utf-8') as publishers_file:
        next(publishers_file)  # Skip header
        cursor.copy_from(publishers_file, 'publishers', sep=',', columns=('publisherid', 'publishername'))
except psycopg2.Error as e:
    conn.rollback()  # Rollback any changes made during this copy operation
    # Close the cursor and connection
    cursor.close()
    conn.close()
