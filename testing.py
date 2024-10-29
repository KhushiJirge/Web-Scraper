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

print(f"The current month is: {month_dict[month]}\n")

url = f"https://canadianauthors.org/national/links/awards-competitions/awards-competitions-{month_dict[month]}-deadlines/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    s = soup.find('div', class_='wf-container-main')
    headings = s.find_all(['h3', 'p'])  # Capture both <h3> and <p> elements

    for item in headings:
        if item.name == 'h3':
            # Print the heading
            print(f"Title: {item.get_text(strip=True)}\n")

        elif item.name == 'p':
            if item.find('strong'):  # Check if there's a strong tag
                # Function to safely get text from next sibling
                def get_sibling_text(sibling):
                    if sibling:
                        if isinstance(sibling, str):
                            return sibling.strip()
                        else:
                            return sibling.get_text(strip=True)
                    return ''

                # Print the genre
                genre = item.find('strong', string='Genre:')
                if genre:
                    genre_text = get_sibling_text(genre.next_sibling)
                    print(f"Genre:       {genre_text}")

                # Print the entry fee
                entry_fee = item.find('strong', string='Entry Fee:')
                if entry_fee:
                    entry_fee_text = get_sibling_text(entry_fee.next_sibling)
                    print(f"Entry Fee:       {entry_fee_text}")

                # Print the deadline
                deadline = item.find('strong', string='Deadline:')
                if deadline:
                    deadline_text = get_sibling_text(deadline.next_sibling)
                    print(f"Deadline:       {deadline_text}")

                # Print the prize
                prize = item.find('strong', string='Prize:')
                if prize:
                    prize_text = get_sibling_text(prize.next_sibling)
                    print(f"Prize:       {prize_text}")

                # Print the description
                description = item.find(lambda tag: tag.name == 'strong' and 'Description:' in tag.get_text(strip=True))
                if description:
                    desc_text = get_sibling_text(description.next_sibling)
                    if desc_text in ['&nbsp;', '']:
                        desc_text = 'No description available.'  # Fallback message
                    print(f"Description:       {desc_text}")

                # Print details link
                details = item.find('strong', string='Details:')
                if details:
                    details_link = details.find_next('a')
                    if details_link:
                        print(f"Details:       {details_link['href']}")

                print("\n" + "="*40 + "\n")  # Separator between entries
