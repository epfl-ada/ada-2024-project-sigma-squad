
EXCEPTIONS_LIST = [
    ('drama','Specialised Drama School'),
    ('dramatic','Specialised Drama School'),
    ('theater','Specialised Drama School'),
    ('theatre','Specialised Drama School'),
    ('performing arts','Specialised Drama School'),
    ('acting','Specialised Acting School'),
    ('film','Specialised Acting School'),
    ('oxford','University of Oxford'),
    ('college cambridge', 'University of Cambridge'),
    ('trinity hall', 'University of Cambridge'),
    ('University of California Los Angeles', "University of California, Los Angeles (UCLA)"),
    ('UCLA', "University of California, Los Angeles (UCLA)"),
    ('University of California Santa Barbara', "University of California, Santa Barbara (UCSB)"),
    ('University College London', 'UCL'),
    ('Kings College London', "King's College London"),
    ('University of Toronto', 'University of Toronto'),
    ('University of Georgia', 'The University of Georgia'),
    ('Harvard', 'University of Harvard'),
    ('University of Missouri', 'University of Missouri'),
    ('University of North Carolina', 'University of North Carolina'),
    ('San Diego State', 'San Diego State University'),
    ('University of Texas', 'University of Texas'),
    ('University of Alabama', 'University of Alabama'),
    ('University of Michigan', 'University of Michigan-Ann Arbor'),
    ('Texas AM', 'Texas A&M University'),
    ('Fordham', 'Fordham University'),
    ('Rutgers', 'Rutgers University–New Brunswick'),
    ('vassar', 'Vassar College'),
    ('Music', 'Specialised Music School'),
    ('Conservatory','Specialised Music School'),
    ('Conservatoire', 'Specialised Music School'),
    ('Juilliard', 'Specialised Music School'),
    ('ballet', 'Specialised Dance School'),
    ('dance', 'Specialised Dance School'),
    ('art', 'Specialised Arts School'),
    ('arts', 'Specialised Arts School')
]

REGION_LIST = [
    ('US', 'USA'),
    ('United States', 'USA'),
    ('Texas', 'USA'),
    ('South Carolina', 'USA'),
    ('Michigan', 'USA'),
    ('Illinois', 'USA'),
    ('Alabama', 'USA'),
    ('Los Angeles', 'USA'),
    ('Indianapolis', 'USA'),
    ('New York', 'USA'),
    ('Virginia', 'USA'),
    ('New Jersey', 'USA'),
    ('Brooklyn', 'USA'),
    ('Tennessee', 'USA'),
    ('Pennsylvania', 'USA'),
    ('Chicago', 'USA'),
    ('Nebraska', 'USA'),
    ('Florida', 'USA'),
    ('Ohio', 'USA'),
    ('Scotland', 'United Kingdom'),
    ('England', 'United Kingdom'),
    ('Wales', 'United Kingdom'),
    ('Ireland', 'United Kingdom'),
    ('Berkshire', 'United Kingdom'),
    ('Frankfurt', 'Europe'),
    ('Germany', 'Europe'),
    ('Spain', 'Europe'),
    ('Netherlands', 'Europe'),
    ('Amsterdam', 'Europe'),
    ('France', 'Europe'),
    ('Iceland', 'Europe'),
    ('Italy', 'Europe'),
    ('Bulgaria', 'Europe'),
    ('Sweden', 'Europe'),
    ('Bosnia', 'Europe'),
    ('Croatia', 'Europe'),
    ('Denmark', 'Europe'),
    ('Slovakia', 'Europe')
]

ETHNICITY_MAPPING = {
    # African Descent
    'African Americans': 'African Descent',
    'Afro-Asians': 'African Descent',
    'Afro-Guyanese': 'African Descent',
    'Nigerian Americans': 'African Descent',
    'Somalis': 'African Descent',
    'Black Canadians': 'African Descent',
    'Black Britons': 'African Descent',
    'Haitian Americans': 'African Descent',
    'Sudanese Arabs': 'African Descent',
    'Ghanaian': 'African Descent',
    'Black Irish': 'African Descent',
    'Afro-Cuban': 'African Descent',
    'Yoruba people': 'African Descent',
    'Ghanaian Americans': 'African Descent',
    'Black people': 'African Descent',
    'Bahamian Americans': 'African Descent',
    'South African Americans': 'African Descent',

    # European Descent
    'Scandinavian Americans': 'European Descent',
    'Portuguese Americans': 'European Descent',
    'German Americans': 'European Descent',
    'Swedish Americans': 'European Descent',
    'Italian Americans': 'European Descent',
    'Irish Americans': 'European Descent',
    'English Americans': 'European Descent',
    'Scottish Americans': 'European Descent',
    'Austrians': 'European Descent',
    'Scottish people': 'European Descent',
    'Irish people': 'European Descent',
    'English people': 'European Descent',
    'White people': 'European Descent',
    'White Americans': 'European Descent',
    'Italians': 'European Descent',
    'Slovak Americans': 'European Descent',
    'Lithuanian Americans': 'European Descent',
    'Anglo-Irish people': 'European Descent',
    'Swedes': 'European Descent',
    'Albanian Americans': 'European Descent',
    'British': 'European Descent',
    'Russian Americans': 'European Descent',
    'Irish migration to Great Britain': 'European Descent',
    'Serbian Americans': 'European Descent',
    'British Americans': 'European Descent',
    'Polish Americans': 'European Descent',
    'French Americans': 'European Descent',
    'Welsh people': 'European Descent',
    'Scotch-Irish Americans': 'European Descent',
    'Dutch Americans': 'European Descent',
    'Greek Canadians': 'European Descent',
    'Irish Australians': 'European Descent',
    'Spaniards': 'European Descent',
    'French': 'European Descent',
    'Germans': 'European Descent',
    'Romani people': 'European Descent',
    'Baltic Russians': 'European Descent',
    'French Canadians': 'European Descent',
    'Catalans': 'European Descent',
    'Czech Americans': 'European Descent',
    'European Americans': 'European Descent',
    'Croatian Americans': 'European Descent',
    'Swedish Canadians': 'European Descent',
    'White British': 'European Descent',
    'Serbian Canadians': 'European Descent',
    'British Jamaicans': 'European Descent',
    'Argentines': 'European Descent',
    'Dutch Australian': 'European Descent',
    'Colombian Americans': 'European Descent',  # Mixed Hispanic/Latino + European
    'Poles': 'European Descent',
    'Russian Canadians': 'European Descent',
    'Rusyn American': 'European Descent',
    'Dutch Canadians': 'European Descent',
    'Polish Australians': 'European Descent',
    'Italian Australians': 'European Descent',
    'Austrians in the United Kingdom': 'European Descent',
    'Bulgarian Canadians': 'European Descent',
    'French Chilean': 'European Descent',
    'German Canadians': 'European Descent',
    'Corsicans': 'European Descent',
    'Sicilian Americans': 'European Descent',
    'Swiss': 'European Descent',
    'Dutch': 'European Descent',
    'English Australians': 'European Descent',
    'Irish Canadians': 'European Descent',
    'Icelanders': 'European Descent',
    'Anglo-Celtic Australians': 'European Descent',
    'Slovene Americans': 'European Descent',
    'Croatian Australians': 'European Descent',
    'British Asians': 'European Descent',
    'British Chinese': 'European Descent',
    'Greek Americans': 'European Descent',
    'Norwegian Americans': 'European Descent',
    'Croats': 'European Descent',
    'Italian Canadians': 'European Descent',
    'Russians': 'European Descent',
    'Hungarian Americans': 'European Descent',
    'Serbs of Croatia': 'European Descent',
    'Welsh Americans': 'European Descent',
    'Spanish Americans': 'European Descent',
    'Danish Americans': 'European Descent',
    'Danes': 'European Descent',
    'Scottish Canadians': 'European Descent',
    'Ukrainian Americans': 'European Descent',
    'Czechs': 'European Descent',
    'Romanian Americans': 'European Descent',
    'Americans': 'European Descent',

    # Jewish Descent
    'Jewish people': 'Jewish Descent',
    'American Jews': 'Jewish Descent',
    'Ashkenazi Jews': 'Jewish Descent',
    'Sephardi Jews': 'Jewish Descent',
    'African-American Jews': 'Jewish Descent',
    'British Jews': 'Jewish Descent',
    'Israeli Americans': 'Jewish Descent',
    'Mizrahi Jews': 'Jewish Descent',
    'History of the Jews in Morocco': 'Jewish Descent',
    'Israelis': 'Jewish Descent',

    # Indigenous Descent
    'Cajun': 'Indigenous Peoples',
    'Cherokee': 'Indigenous Peoples',
    'Māori': 'Indigenous Peoples',
    'Apache': 'Indigenous Peoples',
    'Mohawk': 'Indigenous Peoples',
    'Ojibwe': 'Indigenous Peoples',
    'Choctaw': 'Indigenous Peoples',
    'Lumbee': 'Indigenous Peoples',
    'First Nations': 'Indigenous Peoples',
    'Inuit': 'Indigenous Peoples',
    'Iñupiaq people': 'Indigenous Peoples',
    'Cree': 'Indigenous Peoples',
    'Native Americans in the United States': 'Indigenous Peoples',
    'Blackfoot Confederacy': 'Indigenous Peoples',
    'Native Hawaiians': 'Indigenous Peoples',
    'Indigenous peoples of the Americas': 'Indigenous Peoples',

    # Australian Descent
    'Australians': 'Oceanic Descent',
    'Australian Americans': 'Oceanic Descent',
    'Samoan Americans': 'Oceanic Descent',
    'Kiwi': 'Oceanic Descent',

    # Asian Descent
    'Hongkongers': 'Asian Descent',
    'Japanese Americans': 'Asian Descent',
    'Indians': 'Asian Descent',
    'Chinese Americans': 'Asian Descent',
    'Hmong Americans': 'Asian Descent',
    'Taiwanese Americans': 'Asian Descent',
    'Taiwanese people': 'Asian Descent',
    'Cambodian Americans': 'Asian Descent',
    'Indonesian Americans': 'Asian Descent',
    'Vietnamese Americans': 'Asian Descent',
    'Bengali': 'Asian Descent',
    'Punjabi diaspora': 'Asian Descent',
    'Gujarati people': 'Asian Descent',
    'Filipino mestizo': 'Asian Descent',
    'Filipino people': 'Asian Descent',
    'Indian Americans': 'Asian Descent',
    'Syrian Americans': 'Asian Descent',  # Middle Eastern, but often grouped under broader Asian categories
    'Japanese people': 'Asian Descent',
    'Koreans': 'Asian Descent',
    'Korean Americans': 'Asian Descent',
    'Asian Americans': 'Asian Descent',
    'Asian people': 'Asian Descent',
    'Chinese Canadians': 'Asian Descent',
    'Chinese Singaporeans': 'Asian Descent',
    'Malaysian Chinese': 'Asian Descent',
    'Tamil Americans': 'Asian Descent',

    # Hispanic/Latino Descent
    'Hispanic and Latino Americans': 'Hispanic/Latino Descent',
    'Stateside Puerto Ricans': 'Hispanic/Latino Descent',
    'Cuban Americans': 'Hispanic/Latino Descent',
    'Mexicans': 'Hispanic/Latino Descent',
    'Mexican Americans': 'Hispanic/Latino Descent',
    'Dominican Americans': 'Hispanic/Latino Descent',
    'Venezuelans': 'Hispanic/Latino Descent',
    'Ecuadorian Americans': 'Hispanic/Latino Descent',
    'Salvadoran Americans': 'Hispanic/Latino Descent',
    'Colombians': 'Hispanic/Latino Descent',
    'Bolivian Americans': 'Hispanic/Latino Descent',
    'Spanish people of Filipino ancestry': 'Hispanic/Latino Descent',
    'Puerto Ricans': 'Hispanic/Latino Descent',
    'Criollo people': 'Hispanic/Latino Descent',
    'Brazilian Americans': 'Hispanic/Latino Descent',
    'Hispanics': 'Hispanic/Latino Descent',

    # Mixed or Multiracial
    'multiracial Americans': 'Mixed/Multiracial',
    'Afro Trinidadians and Tobagonians': 'Mixed/Multiracial',
    'multiracial people': 'Mixed/Multiracial',
    'Indo Caribbeans': 'Mixed/Multiracial',
    'Louisiana Creole people': 'Mixed/Multiracial',
    'Eurasian': 'Mixed/Multiracial',
    'White Africans of European ancestry': 'Mixed/Multiracial',

    # Middle Eastern and North African (MENA) Descent
    'Arab Americans': 'Middle Eastern/North African Descent',
    'Lebanese Americans': 'Middle Eastern/North African Descent',
    'Moroccan Americans': 'Middle Eastern/North African Descent',
    'Arabs in Bulgaria': 'Middle Eastern/North African Descent',
    'Pathani': 'Middle Eastern/North African Descent',
    'Dinka people': 'Middle Eastern/North African Descent',
    'Turkish Americans': 'Middle Eastern/North African Descent',
    'Iranian peoples': 'Middle Eastern/North African Descent',
    'مسح': 'Middle Eastern/North African Descent',

}