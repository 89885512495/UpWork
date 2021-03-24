"""
- Create a script called amazon.py

- The script should include a function called scrape().

- The function should accept a single parameter: the link to an amazon product.
"""
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def scrape(url):
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'referer': 'https://www.google.com/'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    user_name = soup.find_all('span', 'a-profile-name')
    user_stars = soup.find_all('span', 'a-icon-alt')
    user_review = soup.find_all('span', 'review-text-content')

    for name, stars, review in zip(user_name, user_stars, user_review):
        data.append({
            'Name': name.get_text(strip=True),
            'Stars': stars.get_text(strip=True),
            'Review': review.get_text(strip=True)
        })
    return data


if __name__ == '__main__':
    for i in range(1, 121):
        reviews = scrape(f"https://www.amazon.com/Sennheiser-Momentum-Cancelling-Headphones-Functionality/"
                         f"product-reviews/B07VW98ZKG/ref=cm_cr_arp_d_paging_btm_next_11?ie=UTF8&reviewerType="
                         f"all_reviews&pageNumber={i}")
        if not reviews:
            break
        pprint(reviews)
