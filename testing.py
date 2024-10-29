import requests
from bs4 import BeautifulSoup
import datetime
import json

date = datetime.datetime.now()
month = date.month

month_dict = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december"
}

url = f"https://canadianauthors.org/national/links/awards-competitions/awards-competitions-{month_dict[month]}-deadlines/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    s = soup.find('div', class_='wf-container-main')
    headings = s.find_all(['h3', 'p'])  

    awards_data = [] 

    for item in headings:
        if item.name == 'h3':
            title = item.get_text(strip=True)

        elif item.name == 'p':
            if item.find('strong'): 

                def get_sibling_text(sibling):
                    if sibling:
                        if isinstance(sibling, str):
                            return sibling.strip()
                        else:
                            return sibling.get_text(strip=True)
                    return ''


                award_entry = {
                    'title': title,
                    'genre': None,
                    'entry_fee': None,
                    'deadline': None,
                    'prize': None,
                    'description': None,
                    'details_link': None
                }


                genre = item.find(lambda tag: tag.name == 'strong' and 'Genre:' in tag.get_text(strip=True))
                if genre:
                    award_entry['genre'] = get_sibling_text(genre.next_sibling)


                entry_fee = item.find(lambda tag: tag.name == 'strong' and 'Entry Fee:' in tag.get_text(strip=True))
                if entry_fee:
                    award_entry['entry_fee'] = get_sibling_text(entry_fee.next_sibling)


                deadline = item.find(lambda tag: tag.name == 'strong' and 'Deadline:' in tag.get_text(strip=True))
                if deadline:
                    award_entry['deadline'] = get_sibling_text(deadline.next_sibling)


                prize = item.find(lambda tag: tag.name == 'strong' and 'Prize:' in tag.get_text(strip=True))
                if prize:
                    award_entry['prize'] = get_sibling_text(prize.next_sibling)


                description = item.find(lambda tag: tag.name == 'strong' and 'Description:' in tag.get_text(strip=True))
                if description:
                    award_entry['description'] = get_sibling_text(description.next_sibling)


                details = item.find(lambda tag: tag.name == 'strong' and 'Details:' in tag.get_text(strip=True))
                if details:
                    details_link = details.find_next('a')
                    if details_link:
                        award_entry['details_link'] = details_link['href']


                awards_data.append(award_entry)

    with open('awards_data.json', 'w') as json_file:
        json.dump(awards_data, json_file, indent=4)

else:
    print(f"Failed to retrieve data: {response.status_code}")
