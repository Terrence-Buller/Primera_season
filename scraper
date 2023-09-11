import requests
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector

### Mappings ###
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

### Season 2000/2001 ###
site_numbers = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22",
                "23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42",
                "43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","78","79","80"]
years = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
for year in years:
    for number in site_numbers:

        ### url + year same 2000-2009 ###
        chosenyear = year
        chosenyear1 = int(str(chosenyear)[-2:]) + 1
        chosenyear1_formatted = f"{chosenyear1:02}"

        url_variable = f"{chosenyear}-{chosenyear1_formatted}"
        # url = f"https://www.bdfutbol.com/en/t/t{url_variable}20{number}.html"
        url = f"https://www.bdfutbol.com/en/t/t{url_variable}{number}.html"



        till_year = int(chosenyear)+1
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
        amount_manager = soup.find_all("table" , class_="taula_estil mb-3")
        total_tr_elements = 0
        for table_element in amount_manager:
            tr_elements = table_element.find_all("tr")
            total_tr_elements += len(tr_elements)
            xyz = len(tr_elements)
            xyz_i = xyz-1
            xyz_r = (xyz_i*2)+5
            soup_list = soup.find_all("td", class_="fit")

            ### Country_names ### [1:] amount of coaches ###
            country_names = soup.find_all("div", class_="pais")[xyz_i:]
            countries = [country_mapping.get(country["class"][1], country["class"][1]) for country in country_names]
            # print(countries)
            # print(len(countries))

            ### Player_Names ### [1:] amount of coaches
            player_names = soup.find_all("span", class_="d-none d-md-block float-left")[xyz_i:]
            players = [player.get_text(strip=True) for player in player_names]
            # print(players)
            # print(len(players))

            ### Position ###
            position_names = soup.find_all("div", class_="fit")
            positions = [position_mapping.get(position["class"][1], position["class"][1]) for position in position_names]
            # print(positions)
            # print(len(positions))

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
            print(numbers)
            print(len(numbers))

            ### Age ###
            age_list = soup.find_all("td", class_="fit font-weight-bold vora-right")
            age = [int(age.get_text(strip=True)) for age in age_list]
            print(age)
            print(len(age))

            specific_th = soup.find('th', class_='fit', title='Called up (without playing)')

            if specific_th:
                ### Played Matches
                pm_numbers = [int(td.get_text()) for td in soup_list[xyz_r::14] if td.get_text().strip() != '']
                # print(pm_numbers)
                # print(len(pm_numbers))

                ### Started Matches ###
                sm_numbers = [int(td.get_text()) for td in soup_list[xyz_r+1::14] if td.get_text().strip() != '']
                # print(pm_numbers)
                # print(len(pm_numbers))

                ### Complete Matches ###
                cm_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+2::14] if td.get_text().strip() != '']
                # print(cm_numbers)
                # print(len(cm_numbers))

                ### Subsitute Matches ###
                sub_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+3::14] if td.get_text().strip() != '']
                # print(sub_numbers)
                # print(len(sub_numbers))

                ### Played minutes ###
                min_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+5::14] if td.get_text().strip() != '']
                # print(min_numbers)
                # print(len(min_numbers))

                ### Yellow cards ###
                yel_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+6::14] if td.get_text().strip() != '']
                # print(yel_numbers)
                # print(len(yel_numbers))

                ### Red cards ###
                red_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+7::14] if td.get_text().strip() != '']
                # print(red_numbers)
                # print(len(red_numbers))

                ### Goals ###
                goals_numbers = [int(td.get_text()) for td in soup_list[xyz_r+8::14] if td.get_text().strip() != '']
                goals_numbers2 = [0 if num <= 0 else num for num in goals_numbers]
                # print(goals_numbers2)
                # print(len(goals_numbers2))

                ### Goalie Goals Against ###
                goals_against = ['-' if (isinstance(num, int) and num >= 0) else abs(num) for num in goals_numbers]
                print(f"Number of players: {len(players)}")



            else:
                ### Played Matches
                pm_numbers = [int(td.get_text()) for td in soup_list[xyz_r::13] if td.get_text().strip() != '']
                # print(pm_numbers)
                # print(len(pm_numbers))

                ### Started Matches ###
                sm_numbers = [int(td.get_text()) for td in soup_list[xyz_r+1::13] if td.get_text().strip() != '']
                # print(sm_numbers)
                # print(len(sm_numbers))

                ### Complete Matches ###
                cm_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+2::13] if td.get_text().strip() != '']
                # print(cm_numbers)
                # print(len(cm_numbers))

                ### Subsitute Matches ###
                sub_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+3::13] if td.get_text().strip() != '']
                # print(sub_numbers)
                # print(len(sub_numbers))

                ### Played minutes ###
                min_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+4::13] if td.get_text().strip() != '']
                # print(min_numbers)
                # print(len(min_numbers))

                ### Yellow cards ###
                yel_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+5::13] if td.get_text().strip() != '']
                # print(yel_numbers)
                # print(len(yel_numbers))

                ### Red cards ###
                red_numbers  = [int(td.get_text()) for td in soup_list[xyz_r+6::13] if td.get_text().strip() != '']
                # print(red_numbers)
                # print(len(red_numbers))

                ### Goals ###
                goals_numbers = [int(td.get_text()) for td in soup_list[xyz_r+7::13] if td.get_text().strip() != '']
                goals_numbers2 = [0 if num <= 0 else num for num in goals_numbers]
                # print(goals_numbers2)
                # print(len(goals_numbers2))

                ### Goalie Goals Against ###
                goals_against = ['-' if (isinstance(num, int) and num >= 0) else abs(num) for num in goals_numbers]
                # print(goals_against)
                # print(len(goals_against))
                print(f"Number of players: {len(players)}")



            df = pd.DataFrame({
                "Name": players,
                "Country": countries,
                "Position": positions,
                "#": numbers,
                "Age": age,
                "Played Matches": pm_numbers,
                "Started Matches": sm_numbers,
                "Completed Matches": cm_numbers,
                "Substitute Matches": sub_numbers,
                "Minutes Played": min_numbers,
                "Yellow cards": yel_numbers,
                "Red Cards": red_numbers,
                "Goals": goals_numbers2,
                "Goals Against": goals_against
            })

            ### main squad/ substitute ###
            df["Status"] = "Substitute"
            df.loc[:10, "Status"] = "Lineup"
            df['year'] = year_names_list
            df['club'] = club_value

            ### change column order
            data = df.reindex(columns=["year", "club","Status", "#", "Name", "Country", "Age", "Played Matches", "Started Matches",
                                        "Completed Matches", "Substitute Matches", "Minutes Played", "Yellow cards", "Red Cards",
                                        "Goals", "Goals Against"])


            ## connect ###
            mydb = mysql.connector.connect(
                host="***",
                user="***",
                password="***",
                database = "***")


            mycursor = mydb.cursor()
            for i, row in data.iterrows():
                sql = "INSERT INTO Club_players (Year, Club, Status, Number, Name, Country, Age, Played_Matches, Started_Matches, Completed_Matches, " \
                          "Substitute_Matches, Minutes_Played, Yellow_Cards, Red_Cards, Goals, Goals_Against) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (row["year"], row["club"], row["Status"], row["#"], row["Name"], row["Country"], row["Age"],
                          row["Played Matches"], row["Started Matches"], row["Completed Matches"], row["Substitute Matches"],
                          row["Minutes Played"], row["Yellow cards"], row["Red Cards"], row["Goals"], row["Goals Against"])
                mycursor.execute(sql, values)

            mydb.commit()
