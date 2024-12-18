import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


## Ethnicity mapping used
ethnicity_mapping = {
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


def encode_categorical(df, columns):
    return pd.get_dummies(df, columns=columns)


"""
Calculate and display the correlation of all features with the 'Success Score' in the given DataFrame.
"""
def display_correlation(df, plot=False):
    corr = df.corr()
    corr_success = corr['Success Score']
    corr_success = corr_success.sort_values(ascending=False)
    corr_success = corr_success.drop('Success Score')
    return corr_success


def ethnicity_to_group(df):
    df.Ethnicity = df.Ethnicity.map(ethnicity_mapping)
    df = df.dropna(subset=['Ethnicity'])
    return df


