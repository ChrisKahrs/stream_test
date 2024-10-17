import streamlit as st
import numpy as np
import json
import requests

# Fake JSON data as if coming from an API
fake_api_response = '''
{
    "data": [
        [2, 1, 3, 1, 1, 4, 0],
        [5, 1, 1, 1, 3, 1, 1],
        [1, 2, 1, 1, 5, 1, 0],
        [1, 1, 4, 1, 2, 3, 1],
        [1, 1, 1, 3, 1, 1, 5],
        [1, 5, 1, 4, 5, 1, 0]
    ],
    "total_score": {
        "player_1": 42
    }
}'''

# Parse the JSON data
api_data = json.loads(fake_api_response)
data = np.array(api_data['data'])

# Text box for match ID
match_id = st.text_input('Enter Match ID:', '')

# Button to submit game state to API
if st.button('Submit Game State') and match_id:
    url = f'https://ckfastapi.azurewebsites.net/match/{match_id}'
    game_state = {
        "board": data.tolist(),
        "total_score": api_data['total_score']
    }
    try:
        response = requests.post(url, json=game_state)
        if response.status_code == 200:
            updated_data = response.json()['board']
            data = np.array(updated_data)
            st.success('Game state updated successfully!')
        else:
            st.error(f'Failed to update game state. Status code: {response.status_code}')
    except requests.RequestException as e:
        st.error(f'Error connecting to the server: {e}')

# Set up the dimensions of the table
rows, cols = data.shape

# Count the number of stars, hearts, diamonds, moons, and triangles
star_count = 0
heart_count = 0
diamond_count = 0
moon_count = 0
triangle_count = 0

# Create HTML table
html_table = "<table style='border-collapse: collapse; width: 100%;'>"

# Create table rows or columns based on view mode
if st.session_state['view_mode'] == 'vertical':
    for row in data:
        html_table += "<tr>"
        for cell in row:
            if cell == 1:
                symbol = '⭐'
                color = "blue"
                star_count += 1
            elif cell == 2:
                symbol = '❤️'
                color = "red"
                heart_count += 1
            elif cell == 3:
                symbol = '🔷'
                color = "yellow"
                diamond_count += 1
            elif cell == 4:
                symbol = '🌙'
                color = "green"
                moon_count += 1
            elif cell == 5:
                symbol = '🔺'
                color = "orange"
                triangle_count += 1
            else:
                symbol = ''
                color = "white"
            html_table += f"<td style='border: 2px solid black; padding: 10px; text-align: center; font-size: 18px;'>"
            if symbol:
                html_table += f"<span style='display: inline-block; width: 50px; height: 50px; border-radius: 50%; background-color: {color}; line-height: 50px; vertical-align: middle;'>{symbol}</span>"
            html_table += "</td>"
        html_table += "</tr>"
else:
    for col in range(cols):
        html_table += "<tr>"
        for row in range(rows):
            cell = data[row, col]
            if cell == 1:
                symbol = '⭐'
                color = "blue"
                star_count += 1
            elif cell == 2:
                symbol = '❤️'
                color = "red"
                heart_count += 1
            elif cell == 3:
                symbol = '🔷'
                color = "yellow"
                diamond_count += 1
            elif cell == 4:
                symbol = '🌙'
                color = "green"
                moon_count += 1
            elif cell == 5:
                symbol = '🔺'
                color = "orange"
                triangle_count += 1
            else:
                symbol = ''
                color = "white"
            html_table += f"<td style='border: 2px solid black; padding: 10px; text-align: center; font-size: 18px;'>"
            if symbol:
                html_table += f"<span style='display: inline-block; width: 50px; height: 50px; border-radius: 50%; background-color: {color}; line-height: 50px; vertical-align: middle;'>{symbol}</span>"
            html_table += "</td>"
        html_table += "</tr>"

html_table += "</table>"

# Prepare player data for score summary table
players = [
    {"player_number": 1, "player_symbol": '⭐', "recent_score": star_count, "total_score": api_data['total_score'].get('player_1', 'N/A')},
    {"player_number": 2, "player_symbol": '❤️', "recent_score": heart_count, "total_score": 'N/A'},
    {"player_number": 3, "player_symbol": '🔷', "recent_score": diamond_count, "total_score": 'N/A'},
    {"player_number": 4, "player_symbol": '🌙', "recent_score": moon_count, "total_score": 'N/A'},
    {"player_number": 5, "player_symbol": '🔺', "recent_score": triangle_count, "total_score": 'N/A'}
]

# Sort players by total score first, then by recent score
players.sort(key=lambda x: (x['total_score'] if isinstance(x['total_score'], int) else 0, x['recent_score']), reverse=True)

# Add score summary table
score_table = "<table style='border-collapse: collapse; width: 100%; margin-top: 20px;'>"
score_table += "<tr><th style='border: 2px solid black; padding: 10px; background-color: lightgrey;'>Player Number</th><th style='border: 2px solid black; padding: 10px; background-color: lightgrey;'>Player Symbol</th><th style='border: 2px solid black; padding: 10px; background-color: lightgrey;'>Recent Score</th><th style='border: 2px solid black; padding: 10px; background-color: lightgrey;'>Total Score</th></tr>"
for player in players:
    score_table += f"<tr><td style='border: 2px solid black; padding: 10px; text-align: center;'>{player['player_number']}</td><td style='border: 2px solid black; padding: 10px; text-align: center;'>{player['player_symbol']}</td><td style='border: 2px solid black; padding: 10px; text-align: center;'>{player['recent_score']}</td><td style='border: 2px solid black; padding: 10px; text-align: center;'>{player['total_score']}</td></tr>"
score_table += "</table>"

# Display the HTML table in Streamlit
st.markdown(html_table, unsafe_allow_html=True)
st.markdown(score_table, unsafe_allow_html=True)