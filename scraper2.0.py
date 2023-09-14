import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from urllib.parse import quote_plus

country_mapping = {
"escocia": "Scotland", "francia": "France", 'inglaterra': "England", "irlanda": "Ireland", "gales": "Wales",
"holanda": "Netherlands", 'noruega': "Norway", 'trinidadytobago': 'Trinidad and Tobago',
'sudafrica': 'South Africa', 'estadosunidos': 'United States'   , 'irlandadelnorte': 'Northern Ireland',
'suecia': 'Sweden', 'australia': 'Australia', 'republicacheca': 'Czech Republic', 'togo': 'Togo', 'espanya': 'Spain',
'brasil': 'Brazil', 'bulgaria': 'Bulgaria', 'camerun': 'Cameroon', 'bielorrusia': 'Belarus', 'belgica': 'Belgium',
'austria': 'Austria', 'argentina': 'Argentina', 'angola': 'Angola', 'alemania' : 'Germany',
'costademarfil': 'Ivory Coast', 'china': 'China', 'coreadelsur': 'South Korea', 'uruguay': 'Uruguay',
'ucrania': 'Ukraine', 'suiza': 'Switzerland', 'serbia': 'Serbia', 'senegal': 'Senegal', 'portugal' : 'Portugal',
'polonia': 'Poland', 'nigeria': 'Nigeria', 'mexico': 'Mexico', 'lituania':'Lithuania', 'liberia': 'Liberia',
'letonia': 'Latvia', 'japon': 'Japan', 'italia': 'Italy', 'grecia': 'Greece', 'ghana': 'Ghana', 'estonia': 'Estonia',
'dinamarca': 'Denmark', 'finlandia': 'Finland', 'jamaica': 'Jamaica', 'iran': 'Iran', "croacia": "Croatia",
"canada": "Canada", "chile": "Chile", "colombia": "Colombia", "congo": "Congo", "ecuador": "Ecuador",
"georgia": "Georgia", "guadalupe": "France(guadalupe)", "guinea": "Guinea", "guineaecuatorial": "Equatorial Guinea",
"islandia": "Iceland", "israel": "Israel", "mali": "Mali", "marruecos": "Marocco", "nuevazelanda": "New Zealand",
"paraguay": "Paraguay", "peru": "Peru", "rumania": "Romania", "seychelles": "Seychelles", "sierraleona": "Sierra Leone",
"turquia": "Turkey", "uganda": "Uganda", "eslovaquia": "Slovakia", "honduras": "Honduras", "eslovenia": "Slovenia",
"bermudas": "Bermuda", "guatemala": "Guatemala", "chipre": "Cyprus", "costarica": "Costa Rica", "bosnia": "Bosnia",
"barbados": "Barbados", "macedonia": "Macedonia", "antigua": "Antigua", "zambia": "Zambia", "zimbabwe": "Zimbabwe",
"tunez": "Tunisia", "oman": "Oman", "grenada": "Grenada", "hungria": "Hungary", "egipto": "Egypt", "argelia": "Algeria",
"rusia": "Russia", "gabon": "Gabon", "caboverde": "Cape Verde", "curazao": "Curaçao", "surinam": "Suriname",
"martinica": "Martinique", "republicadelcongo" : "Republic of the Congo", "islasferoe": "Faroe Islands",
"bolivia": "Bolivia", "venezuela": "Venezuela", "madagascar": "Madagascar", "panama": "Panama",
"montenegro": "Montenegro", "mozambique": "Mozambique", "haiti": "Haiti", "cuba":"Cuba", "kosovo": "Kosovo",
"benin":"Benin", "arabiasaudi": "Saudi Arabia", "mauritania": "Mauritania", "qatar": "Qatar", "armenia": "Armenia",
"azerbaijan": "Azerbaijan", "tailandia": "Thailand", "republicadominicana": "Dominican Republic", "albania": "Albania",
"republicacentroafricana": "Central African Republic", "guineabissau": "Guinea-Bissau", "kenia": "Kenia",
"gambia":"Gambia", "burkinafaso": "Burkinafaso", "chad": "Chad", "eritrea": "Eritrea", "burundi": "Burundi",
"andorra": "Andorra"}

position_mapping = {
"por": "Goal keeper", 'ltd': 'Right-back', 'lti': 'Left-back', 'cen': 'Centre-back', 'def': 'Defender',
'mig': 'Midfield', 'dav': 'Striker', 'dac': 'Forward'}

Column_names = {0: 'Country', 1: 'Name', 2: 'Position', 3: 'Number', 4: 'Age', 5: 'Played_Matches',
                6: 'Started_Matches', 7: 'Completed_Matches', 8: 'Substitute_Matches' ,9: 'Minutes_Played' ,
                10: 'Yellow_Cards', 11: 'Red_Cards', 12: "Goals", 13: "Goals_Against"}

for year in range(2000, 2023):
    for number in range(0, 81):

        ### url + year same 2000-2009 ###
        chosenyear = year
        chosenyear1 = int(str(chosenyear)[-2:]) + 1
        chosenyear1_formatted = f"{chosenyear1:02}"

        url_variable = f"{chosenyear}-{chosenyear1_formatted}"
        url = f"https://www.bdfutbol.com/en/t/t{url_variable}{number}.html"

        till_year = int(chosenyear) + 1
        year_names_list = f"{chosenyear}/{till_year}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Link: {url}: {e} not here")
            continue

        print(number, url)
        soup = BeautifulSoup(response.text, "html.parser")
        ### Club ###
        club_names = soup.find_all("span", class_="heroh1")
        club_names_list = [club.find("a").get_text() for club in club_names]
        club_value = club_names_list[0]
        html = url
        competition_check = [(a.get('href'), a.get_text()) for a in soup.find_all('a')]
        found_condition = False
        for href, text in competition_check:
            if href and 'First Division' in text:
                found_condition = True
                break

        if not found_condition:
            print(f"Site number {number} does not contain 'First Division' in href. Skipping.")
            continue

        ### afwijking aantal managers: ###
        amount_manager = soup.find_all("table", class_="taula_estil mb-3")
        total_tr_elements = 0
        df3 = []
        df2 = []

        for table_element in amount_manager:
            tr_elements = table_element.find_all("tr")
            total_tr_elements += len(tr_elements)
            xyz = len(tr_elements)
            xyz_i = xyz - 1
            xyz_r = (xyz_i * 2) + 5
            soup_list = soup.find_all("td", class_="fit")

            ### Country_names ### [1:] amount of coaches ###
            country_names = soup.find_all("div", class_="pais")[xyz_i:]
            countries = [country_mapping.get(country["class"][1], country["class"][1]) for country in country_names]
            df3.append(countries)

            ### Player_Names ### [1:] amount of coaches
            player_names = soup.find_all("span", class_="d-none d-md-block float-left")[xyz_i:]
            players = [player.get_text(strip=True) for player in player_names]
            df3.append(players)

            ### Position ###
            position_names = soup.find_all("div", class_="fit")
            positions = [position_mapping.get(position["class"][1], position["class"][1]) for position in position_names]
            df3.append(positions)

            ### Number ###
            elements_number = soup.find_all(["td", "div"], class_=["fit text-right pr-0", "vora-left-div filial"])
            element_dict = {}

            # Loop through the elements and assign each one a unique identifier
            for idx, element in enumerate(elements_number):
                element_dict[element] = idx

            # Initialize an empty list to store the extracted numbers and their corresponding unique identifiers
            number_elements = []

            # Loop through the elements and extract numbers along with their identifiers
            for element in elements_number:
                text = element.get_text(strip=True)
                if text.isdigit():
                    number = int(text)
                else:
                    number = 0
                number_elements.append((number, element_dict[element]))

            # Sort the list of tuples by the unique identifiers
            number_elements.sort(key=lambda x: x[1])
            numbers = [num for num, _ in number_elements]
            df3.append(numbers)

            ### Age ###
            age_list = soup.find_all("td", class_="fit font-weight-bold vora-right")
            age = [int(age.get_text(strip=True)) for age in age_list]
            df3.append(age)

            specific_th = soup.find('th', class_='fit', title='Called up (without playing)')

            if specific_th:
                for z in range(9):
                    if z == 4:
                        continue

                    code = [int(td.get_text()) for td in soup_list[xyz_r + z::14] if td.get_text().strip() != '']

                    if z == 8:
                        code2 = [0 if num <= 0 else num for num in code]
                        df3.append(code2)

                        code3 = ['-' if (isinstance(num2, int) and num2 >= 0) else abs(num2) for num2 in code]
                        df3.append(code3)

                    else:
                        code = [0 if num1 <= 0 else num1 for num1 in code]
                        df3.append(code)

                df2 = pd.DataFrame(df3)
                df2 = df2.transpose()
                df2 = df2.rename(columns=Column_names)

            else:
                for z in range(8):

                    code = [int(td.get_text()) for td in soup_list[xyz_r + z::13] if td.get_text().strip() != '']

                    if z == 7:
                        code2 = [0 if num <= 0 else num for num in code]
                        df3.append(code2)

                        code3 = ['-' if (isinstance(num2, int) and num2 >= 0) else abs(num2) for num2 in code]
                        df3.append(code3)

                    else:
                        code = [0 if num1 <= 0 else num1 for num1 in code]
                        df3.append(code)

                df2 = pd.DataFrame(df3)
                df2 = df2.transpose()
                df2 = df2.rename(columns=Column_names)


            ### main squad/ substitute ###
            df2["Status"] = "Substitute"
            df2.loc[:10, "Status"] = "Lineup"
            df2['Year'] = year_names_list
            df2['Club'] = club_value


            ### Change column order ###
            data = df2.reindex(
                columns=["Year", "Club", "Status", "Number", "Name", "Country", "Position", "Age", "Played_Matches", "Started_Matches",
                         "Completed_Matches", "Substitute_Matches", "Minutes_Played", "Yellow_Cards", "Red_Cards",
                         "Goals", "Goals_Against"])


            ### SQL Part ###
            password = quote_plus("****")
            engine = create_engine(f"mysql+mysqlconnector://***:{password}@localhost:****/****")
            table_name = 'club_players'
            data.to_sql(table_name, con=engine, if_exists='append', index=False)
