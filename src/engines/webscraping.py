import requests
import random
import time
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

class ActorScraperEngine:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/wiki/"
        pass

    def process_part(self, part):
        """
        Processes a given part of a name string according to specific rules.
        """
        part = part.lower()

        if part.startswith("'") and part.endswith("'"):
            return ''

        # Handle "McSomething"
        if part.startswith('mc'):
            return part[:2].capitalize() + part[2:].capitalize()
        
        # Handle "MacSomething"
        if part.startswith('mac'):
            return part[:3].capitalize() + part[3:].capitalize()
        
        # Handle names with apostrophes, e.g., O'Something
        elif "'" in part:
            subparts = part.split("'")
            return "%27".join([sub.capitalize() for sub in subparts])

        # Handle names with hyphens, e.g., Jean-Claude
        elif '-' in part:
            subparts = part.split('-')
            return '-'.join([sub.capitalize() for sub in subparts])

        # Handle specific cases
        if part == 'von':
            return 'von'
        if part == 'dicaprio':
            return 'DiCaprio'

        # Default capitalization for other parts
        return part.capitalize()
    
    def cap_surnames(self, name):
        """
        Processes the full given name string.
        """
        name = name.replace('_', ' ')
        parts = name.split() # Split name and surname into parts
        parts = [self.process_part(part) for part in parts if self.process_part(part)]
        return ' '.join(parts)
    
    def clean_text(self, text):
        """
        Cleans the input text. Removes special characters.
        """
        # Remove special characters and replace '\n' with ', '
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        cleaned_text = cleaned_text.replace('\n', ', ')
        cleaned_text = cleaned_text.replace('  ', ' ')
        return cleaned_text

    def fetch_wikipedia_data(self, actor_name):
        """
        Fetch actor data from Wikipedia.
        """
        data = self.initialize_data()

        try:
            url = self.construct_url(actor_name)
            response = self.get_response(url)
            if response.status_code != 200:
                print(f"Failed to fetch data for {actor_name}: HTTP {response.status_code}")
                return data

            soup = BeautifulSoup(response.text, 'html.parser')
            data['Gender'] = self.determine_gender(soup)
            infobox = soup.find('table', class_='infobox')
            if infobox:
                self.parse_infobox(infobox, data)

            self.search_sections(soup, data)
            return data

        except Exception as e:
            print(f"Error fetching data for {actor_name}: {e}")
            return data

    def initialize_data(self):
        return {
            'Gender': None,
            'University': None,
            'Theater': None,
            'Sports': None,
            'Birth City': None,
            'Date of Birth': None,
            'Citizenship': None,
            'Number of Children': None,
            'Career Start': None
        }

    def construct_url(self, actor_name):
        return f"{self.base_url}{actor_name.replace(' ', '_')}"

    def get_response(self, url):
        return requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    def determine_gender(self, soup):
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            if paragraph.text.strip():
                intro_text = paragraph.text.lower()
                if 'actor' in intro_text:
                    return 'Male'
                elif 'actress' in intro_text:
                    return 'Female'
                else:
                    he_count = intro_text.count(' he ')
                    she_count = intro_text.count(' she ')
                    if he_count > she_count:
                        return 'Male'
                    elif she_count > he_count:
                        return 'Female'
                break
        return None

    def parse_infobox(self, infobox, data):
        rows = infobox.find_all('tr')
        for row in rows:
            header = row.find('th')
            cell = row.find('td')
            if not header or not cell:
                continue

            header_text = header.text.strip()
            cell_text = cell.text.strip()

            if 'Alma mater' in header_text or 'Alma\xa0mater' in header_text or 'Education' in header_text:
                data['University'] = self.clean_text(cell_text)

            if 'Born' in header_text:
                self.extract_birth_info(cell, data)

            if 'Citizenship' in header_text:
                data['Citizenship'] = self.clean_text(cell_text)

            if 'Children' in header_text:
                match = re.search(r'\d+', cell_text)
                if match:
                    data['Number of Children'] = match.group()

            if 'active' in header_text or 'Career' in header_text:
                match = re.search(r'\b\d{4}\b', cell_text)
                if match:
                    data['Career Start'] = match.group()

    def extract_birth_info(self, cell, data):
        bday = cell.find('span', class_='bday')
        if bday:
            data['Date of Birth'] = bday.text.strip()

        birthplace = cell.find('div', class_='birthplace')
        if birthplace:
            data['Birth City'] = birthplace.text.strip()
        else:
            br_tag = cell.find('br')
            if br_tag:
                if br_tag.next_sibling and br_tag.next_sibling.name == 'a':
                    data['Birth City'] = br_tag.next_sibling.text.strip()
                elif br_tag.next_sibling and isinstance(br_tag.next_sibling, str):
                    data['Birth City'] = br_tag.next_sibling.strip()
                else:
                    all_br_tags = cell.find_all('br')
                    if all_br_tags:
                        last_br_tag = all_br_tags[-1]
                        if last_br_tag.next_sibling and isinstance(last_br_tag.next_sibling, str):
                            data['Birth City'] = last_br_tag.next_sibling.strip()
                        elif last_br_tag.next_sibling and last_br_tag.next_sibling.name == 'a':
                            data['Birth City'] = last_br_tag.next_sibling.next_sibling.strip()
        data['Birth City'] = self.clean_text(data['Birth City'])

    def search_sections(self, soup, data):
        sports_keywords = ['soccer', 'football', 'basketball', 'baseball', 'tennis', 'track', 'swimming', 'martial arts', 'ballet', 'dance']
        theater_keywords = ['theater', 'theatre']
        university_keywords = ['university', 'college', 'academy', 'institute', 'school']

        self.search_early_life_section(soup, data, sports_keywords, theater_keywords, university_keywords)
        self.search_career_section(soup, data, sports_keywords, theater_keywords)
        self.search_body_content(soup, data, sports_keywords, theater_keywords, university_keywords)

    def search_early_life_section(self, soup, data, sports_keywords, theater_keywords, university_keywords):
        early_life = soup.find('h2', {'id': lambda x: x and 'early_life' in x.lower()})
        if early_life:
            data['Sports'] = self.search_section(early_life.find_parent(), sports_keywords)
            data['Theater'] = 'Yes' if self.search_section(early_life.find_parent(), theater_keywords) else data['Theater']
            if not data['University']:
                data['University'] = self.search_section(early_life, university_keywords)

    def search_career_section(self, soup, data, sports_keywords, theater_keywords):
        career_section = soup.find('h2', {'id': lambda x: x and 'career' in x.lower()})
        if career_section:
            data['Sports'] = data['Sports'] or self.search_section(career_section.find_parent(), sports_keywords)
            data['Theater'] = data['Theater'] or ('Yes' if self.search_section(career_section.find_parent(), theater_keywords) else None)

    def search_body_content(self, soup, data, sports_keywords, theater_keywords, university_keywords):
        body_content = soup.find('div', {'class': 'mw-parser-output'})
        if body_content:
            if not (data['Theater'] or data['Sports']):
                self.search_paragraphs(body_content, data, sports_keywords, theater_keywords)

            if not data['University']:
                self.search_university(body_content, data, university_keywords)

    def search_paragraphs(self, body_content, data, sports_keywords, theater_keywords):
        for paragraph in body_content.find_all('p', recursive=False):
            text = paragraph.text.lower()
            for keyword in sports_keywords:
                if keyword in text:
                    data['Sports'] = keyword.capitalize()
                    break
            for keyword in theater_keywords:
                if keyword in text:
                    data['Theater'] = 'Yes'
                    break

    def search_university(self, body_content, data, university_keywords):
        for paragraph in body_content.find_all('p', recursive=False):
            text = paragraph.text.lower()
            for keyword in university_keywords:
                if keyword in text:
                    if keyword == 'academy':
                        matches = re.finditer(r'\bacademy\b', text)
                        for match in matches:
                            start_index = match.end()
                            if not text[start_index:].strip().lower().startswith('award'):
                                link = paragraph.find('a', string=re.compile(r'\bacademy\b', re.IGNORECASE))
                                if link:
                                    data['University'] = link.text.strip()
                                else:
                                    data['University'] = 'Academy'
                                break
                    else:
                        link = paragraph.find('a', string=re.compile(rf'\b{keyword}\b', re.IGNORECASE))
                        if link:
                            data['University'] = link.text.strip()
                        else:
                            data['University'] = keyword.capitalize()
                        break

    def search_section(self, section, keywords):
        for sibling in section.find_next_siblings():
            if sibling.name in ['div', 'h2', 'h3']:
                break
            if sibling.name == 'p':
                paragraph_text = sibling.text.lower()
                for keyword in keywords:
                    if keyword in paragraph_text:
                        return keyword.capitalize()
        return None
            
        
    def test_one_actor(self, actor_name):
        """
        Test the Wikipedia scraper on a single actor.
        """
        data = self.fetch_wikipedia_data(actor_name)
        print(f"Data for {actor_name}: {data}")
        return
    

    def run_scraping(self, actor_df):
        """
        Run the Wikipedia scraper on all actors in the dataset.
        """
        actor_df.index = actor_df.index.map(self.cap_surnames)

        # Add new columns to the dataframe
        new_columns = ['University', 'Theater', 'Sports', 'Birth City', 'Citizenship', 'Number of Children']
        for col in new_columns:
            actor_df.loc[:, col] = None

        # Main loop for scraping
        for idx, row in tqdm(actor_df.iterrows(), total=len(actor_df)):
            actor_name = row.name  # Adjust column name as per your dataset
            actor_data = self.fetch_wikipedia_data(actor_name)

            # Update the dataframe with the fetched data
            for col in new_columns:
                actor_df.loc[idx, col] = actor_data[col]

            # Respectful scraping: Introduce delay
            time.sleep(random.uniform(1, 3))

        return


