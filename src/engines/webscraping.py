import requests
import random
import time
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

class ActorScraperEngine:
    def __init__(self):
        pass

    def _cap_surnames(self, name):
        name = name.replace('_', ' ')
        parts = name.split() # Split name and surname into parts
        
        # Process each part of the name
        for i in range(len(parts)):
            part = parts[i].lower()

            # Remove nicknames in single quotes
            if part.startswith("'") and part.endswith("'"):
                parts[i] = ''  # Mark the nickname for removal
                continue

            # Handle "McSomething"
            if part.startswith('mc'):
                parts[i] = part[:2].capitalize() + part[2:].capitalize()

            # Handle "MacSomething"
            elif part.startswith('mac'):
                parts[i] = part[:3].capitalize() + part[3:].capitalize()

            # Handle names with apostrophes, e.g., O'Something
            elif "'" in part:
                subparts = part.split("'")
                parts[i] = "%27".join([sub.capitalize() for sub in subparts])

            # Handle names with hyphens, e.g., Jean-Claude
            elif '-' in part:
                subparts = part.split('-')
                parts[i] = '-'.join([sub.capitalize() for sub in subparts])

            # Handle "von" (do not capitalize "von")
            elif part == 'von':
                parts[i] = 'von'
            
            # Handle Leo
            elif part == 'dicaprio':
                parts[i] = 'DiCaprio'

            # Default capitalization for other parts
            else:
                parts[i] = part.capitalize()

        # Remove empty parts (e.g., nicknames marked as '')
        parts = [part for part in parts if part]

        return ' '.join(parts)
    

    def _clean_text(self, text):
        # Remove special characters and replace '\n' with ', '
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        cleaned_text = cleaned_text.replace('\n', ', ')
        cleaned_text = cleaned_text.replace('  ', ' ')
        return cleaned_text
    

    def _fetch_wikipedia_data(self, actor_name):
        """
        Fetch actor data from Wikipedia.
        """
        data = {    
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
        
        try:
            # Construct the Wikipedia URL
            url = f"https://en.wikipedia.org/wiki/{actor_name.replace(' ', '_')}"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            
            # Check for a successful request
            if response.status_code != 200:
                print(f"Failed to fetch data for {actor_name}: HTTP {response.status_code}")
                return data
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Determine Gender
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                #print(paragraph.text)
                if paragraph.text.strip():  # Check if the paragraph is not empty
                    intro_text = paragraph.text.lower()
                    if 'actor' in intro_text:
                        data['Gender'] = 'Male'
                    elif 'actress' in intro_text:
                        data['Gender'] = 'Female'
                    else:
                        he_count = intro_text.count(' he ')
                        she_count = intro_text.count(' she ')
                        if he_count > she_count:
                            data['Gender'] = 'Male'
                        elif she_count > he_count:
                            data['Gender'] = 'Female'
                    break  # Use the first non-empty paragraph

            # Locate the infobox
            infobox = soup.find('table', class_='infobox')
            #print('infobox found:', infobox)
            
            if infobox:
                rows = infobox.find_all('tr')
                for row in rows:
                    header = row.find('th')
                    cell = row.find('td')
                    if not header or not cell:
                        continue
                    
                    header_text = header.text.strip()
                    cell_text = cell.text.strip()

                    # Debugging print statements
                    #print(f"Header: {header_text}")
                    #print(f"Cell: {cell_text}")
                    
                    # University
                    if 'Alma mater' in header_text or 'Alma\xa0mater' in header_text or 'Education' in header_text:
                        university = self._clean_text(cell_text)
                        data['University'] = university

                    
                    if 'Born' in header_text:
                        # Extract Date of Birth
                        bday = cell.find('span', class_='bday')
                        if bday:
                            data['Date of Birth'] = bday.text.strip()
                        
                        # Birth City
                        birthplace = cell.find('div', class_='birthplace')
                        if birthplace:
                            data['Birth City'] = birthplace.text.strip()
                        else:
                            # Check for text after <br>
                            br_tag = cell.find('br')
                            if br_tag:
                                # If the next sibling is an HTML tag, extract its text
                                if br_tag.next_sibling and br_tag.next_sibling.name == 'a':
                                    data['Birth City'] = br_tag.next_sibling.text.strip()
                                # If it's just a string, extract it directly
                                elif br_tag.next_sibling and isinstance(br_tag.next_sibling, str):
                                    data['Birth City'] = br_tag.next_sibling.strip()
                                else:
                                    # If there are multiple <br> tags, get the last one
                                    all_br_tags = cell.find_all('br')
                                    if all_br_tags:
                                        last_br_tag = all_br_tags[-1]
                                        if last_br_tag.next_sibling and isinstance(last_br_tag.next_sibling, str):
                                            data['Birth City'] = last_br_tag.next_sibling.strip()
                                        elif last_br_tag.next_sibling and last_br_tag.next_sibling.name == 'a':
                                            data['Birth City'] = last_br_tag.next_sibling.next_sibling.strip()
                        data['Birth City'] = self._clean_text(data['Birth City'])
                    
                    # Citizenship
                    if 'Citizenship' in header_text:
                        citizenship = self._clean_text(cell_text)
                        data['Citizenship'] = citizenship

                    # Number of Children
                    if 'Children' in header_text:
                        match = re.search(r'\d+', cell_text)
                        if match:
                            data['Number of Children'] = match.group()
                    
                    # Career Start
                    if 'active' in header_text or 'Career' in header_text:
                        match = re.search(r'\b\d{4}\b', cell_text)  # Look for a 4-digit year
                        if match:
                            data['Career Start'] = match.group()

                    # Helper function to search sections for keywords
            def search_section(section, keywords):
                for sibling in section.find_next_siblings():
                    if sibling.name in ['div', 'h2', 'h3']:  # Reached the next section
                        break
                    if sibling.name == 'p':  # Check paragraphs within the section
                        paragraph_text = sibling.text.lower()
                        for keyword in keywords:
                            if keyword in paragraph_text:
                                return keyword.capitalize()
                return None

            # Sports & Theater
            sports_keywords = ['soccer', 'football', 'basketball', 'baseball', 'tennis', 'track', 'swimming', 'martial arts', 'ballet', 'dance']
            theater_keywords = ['theater', 'theatre']
            university_keywords = ['university', 'college', 'academy', 'institute', 'school']

            # Look in "Early life" section
            early_life = soup.find('h2', {'id': lambda x: x and 'early_life' in x.lower()}) # Look for an "Early life" section
            if early_life:
                data['Sports'] = search_section(early_life.find_parent(), sports_keywords)
                data['Theater'] = 'Yes' if search_section(early_life.find_parent(), theater_keywords) else data['Theater']
                if not data['University']:
                    data['University'] = search_section(early_life, university_keywords)

            # If not found, look in "Career" or similar sections
            career_section = soup.find('h2', {'id': lambda x: x and 'career' in x.lower()})
            if career_section:
                data['Sports'] = data['Sports'] or search_section(career_section.find_parent(), sports_keywords)
                data['Theater'] = data['Theater'] or ('Yes' if search_section(career_section.find_parent(), theater_keywords) else None)

            # If no sections are present, search in the main body
            body_content = soup.find('div', {'class': 'mw-parser-output'})
            if body_content:
                if not (data['Theater'] or data['Sports']):
                    for paragraph in body_content.find_all('p', recursive=False):
                        text = paragraph.text.lower()
            
                        # Check for sports keywords
                        for keyword in sports_keywords:
                            if keyword in text:
                                data['Sports'] = keyword.capitalize()
                                break  # Stop searching once we find a match
            
                        # Check for theater keywords
                        for keyword in theater_keywords:
                            if keyword in text:
                                data['Theater'] = 'Yes'
                                break  # Stop searching once we find a match
    
                if not data['University']:
                    for paragraph in body_content.find_all('p', recursive=False):
                        text = paragraph.text.lower()
            
                        # Check for university keywords
                        for keyword in university_keywords:
                            if keyword in text:
                                if keyword == 'academy':
                                    # Handle "academy" with special logic
                                    matches = re.finditer(r'\bacademy\b', text)
                                    for match in matches:
                                        start_index = match.end()
                                        if not text[start_index:].strip().lower().startswith('award'):
                                            # Check for a link containing 'academy'
                                            link = paragraph.find('a', string=re.compile(r'\bacademy\b', re.IGNORECASE))
                                            if link:
                                                data['University'] = link.text.strip()
                                            else:
                                                data['University'] = 'Academy'
                                            break
                                else:
                                    # Check for a link containing the keyword
                                    link = paragraph.find('a', string=re.compile(rf'\b{keyword}\b', re.IGNORECASE))
                                    if link:
                                        data['University'] = link.text.strip()
                                    else:
                                        data['University'] = keyword.capitalize()
                                    break

            return data

        except Exception as e:
            print(f"Error fetching data for {actor_name}: {e}")
            return data
            
        
    def _test_one_actor(self, actor_name):
        """
        Test the Wikipedia scraper on a single actor.
        """
        data = self._fetch_wikipedia_data(actor_name)
        print(f"Data for {actor_name}: {data}")
        return
    

    def run_scraping(self, actor_df):
        """
        Run the Wikipedia scraper on all actors in the dataset.
        """
        actor_df.index = actor_df.index.map(self._cap_surnames)

        # Add new columns to the dataframe
        new_columns = ['University', 'Theater', 'Sports', 'Birth City', 'Citizenship', 'Number of Children']
        for col in new_columns:
            actor_df.loc[:, col] = None

        # Main loop for scraping
        for idx, row in tqdm(actor_df.iterrows(), total=len(actor_df)):
            actor_name = row.name  # Adjust column name as per your dataset
            actor_data = self._fetch_wikipedia_data(actor_name)

            # Update the dataframe with the fetched data
            for col in new_columns:
                actor_df.loc[idx, col] = actor_data[col]

            # Respectful scraping: Introduce delay
            time.sleep(random.uniform(1, 3))

        return


