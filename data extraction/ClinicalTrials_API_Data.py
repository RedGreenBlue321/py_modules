

import requests
import pandas as pd
import datetime
import logging

logging.basicConfig(level=logging.INFO)

BASE_URL = 'https://clinicaltrials.gov/api/query/study_fields'

FIELDS = [
    'NCTId', 'BriefTitle', 'OfficialTitle', 'Condition', 'StudyType',
    'InterventionName', 'InterventionType', 'EligibilityCriteria',
    'StudyPopulation', 'StudyFirstPostDate'
]

class ClinicalTrials_Data:
    
    def __init__(self, search_term, max_results=100):
        self.search_term = search_term
        self.max_results = max_results
        
    def fetch_trials(self):
        params = {
            "expr": self.search_term,
            "fields": ",".join(FIELDS),
            "min_rnk": 1,
            "max_rnk": self.max_results,
            "fmt": "json"
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for bad HTTP responses
        
        trials_data = response.json()['StudyFieldsResponse']['StudyFields']
        df = self._clean_data(pd.DataFrame(trials_data))
        
        self._save_to_csv(df)
        
        return df

    def _clean_data(self, df):
        for column in df.columns:
            df[column] = df[column].apply(lambda x: '; '.join(x) if isinstance(x, list) and x else x)

        df['StudyFirstPostDate'] = pd.to_datetime(df.StudyFirstPostDate)
        return df.sort_values(by='StudyFirstPostDate', ascending=False)

    def _save_to_csv(self, df):
        timestamp = datetime.datetime.now().date().isoformat()
        filename = f'{self.search_term}_clinical_trials_{timestamp}.csv'
        df.to_csv(filename, index=False)
        logging.info(f"Saved data to {filename}")
        
        interventional_filename = f'{self.search_term}_interventional_clinical_trials_{timestamp}.csv'
        df[df.StudyType == 'Interventional'].to_csv(interventional_filename, index=False)
        logging.info(f"Saved interventional data to {interventional_filename}")


if __name__ == "__main__":
    extract_data = ClinicalTrials_Data("breast+cancer", max_results=200)
    df = extract_data.fetch_trials()


