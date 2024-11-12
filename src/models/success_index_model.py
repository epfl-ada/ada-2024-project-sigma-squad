import pandas as pd
import numpy as np
import sys
import os

# Add the path to the src/data folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))

from transform_data import clean_data


#final_merged_data['Revenue/Budget ratio'] = final_merged_data['Movie box office revenue'] / final_merged_data['Movie budget']


if __name__ == "__main__":
    print(clean_data().head())