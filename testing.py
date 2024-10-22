import requests
from bs4 import BeautifulSoup
import datetime

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
                # Print the genre
                genre = item.find('strong', string='Genre:')
                if genre:
                    print(f"Genre: {genre.next_sibling.strip()}")
                
                # Print the entry fee
                entry_fee = item.find('strong', string='Entry Fee:')
                if entry_fee:
                    print(f"Entry Fee: {entry_fee.next_sibling.strip()}")

                # Print the deadline
                deadline = item.find('strong', string='Deadline:')
                if deadline:
                    print(f"Deadline: {deadline.next_sibling.strip()}")

                # Print the prize
                prize = item.find('strong', string='Prize:')
                if prize:
                    print(f"Prize: {prize.next_sibling.strip()}")

                # Print the description
                description = item.find('strong', string='Description:')
                if description:
                    print(f"Description: {description.next_sibling.strip()}")

                # Print details link
                details = item.find('strong', string='Details:')
                if details:
                    details_link = details.find_next('a')
                    if details_link:
                        print(f"Details: {details_link['href']}")

                print("\n" + "="*40 + "\n")  # Separator between entries
