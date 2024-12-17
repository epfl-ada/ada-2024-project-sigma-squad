# Copyright (c) 2012-2022 Yuanchun Shen

"""
Entity converter converts between Freebase and Wikidata entity IDs.
"""
import requests
from SPARQLWrapper import JSON, SPARQLWrapper

class EntityConverter:
    """A converter to convert between freebase and wikidata entities.
    """
    def __init__(self, endpoint="https://query.wikidata.org/sparql") -> None:
        sparql = SPARQLWrapper(endpoint)
        sparql.setReturnFormat(JSON)
        self.sparql = sparql
        self.ethnicity_data = {} # Dictionary to store the mapping between MIDs and ethnicity labels
        self.seen_mids = set()  # Set to keep track of unique MIDs
    
    def query_wikidata(self, query):
        """Query wikidata

        Args:
            query (str): SPARQL query

        Returns:
            dict: SPARQL query result
        """
        self.sparql.setQuery(query)
        try:
            ret = self.sparql.queryAndConvert()
            return ret
        except Exception as e:
            print(f"Error with query wikidata: {e}")
            return None

    def mid_to_qid(self, entity, limit=1):
        """Convert freebase id to wikidata id

        Args:
            entity (str): Freebase id, e.g. /m/0bwd_0

        Returns:
            str | list[str]: Corresponding wikidata id, e.g. Q42
                If limit is greater than 1, return a list of wikidata ids.
        """
        query = f"""
            SELECT DISTINCT ?qid WHERE {{
                ?qid wdt:P646 "{entity}".
            }}
            LIMIT {limit}
            """
        response = self.query_wikidata(query)
        if response is None or "results" not in response:
            return None
        bindings = response["results"]["bindings"]
        if len(bindings) > 0:
            if limit == 1:
                qid = bindings[0]["qid"]["value"]
                qid = qid.split("/")[-1]
                return qid
            qids = [b["qid"]["value"] for b in bindings]
            qids = [qid.split("/")[-1] for qid in qids]
            return qids
        return None

    def qid_to_ethnicity(self, qid):
        """
        Gets the ethnicity label of a given Wikidata ID using the Wikidata API.

        Args:
            qid (str): The Wikidata ID (e.g., 'Q3267812').

        Returns:
            str: The label of the Wikidata ID.
        """

        url = f"https://www.wikidata.org/w/api.php"
        params = {
            'action': 'wbgetentities',
            'ids': qid,
            'languages': 'en',
            'format': 'json'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Extract the label from the response
            ethnicity = data['entities'].get(qid, {}).get('labels', {}).get('en', {}).get('value')
            if ethnicity:
                return ethnicity
            else:
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {qid}: {e}")
            return None

    def get_ethnicity(self, mid):
        if mid is None:
            return None
        elif mid in self.seen_mids:
            return self.ethnicity_data[mid]
        else:
            self.seen_mids.add(mid)
            qid = self.mid_to_qid(mid)

            if qid is None:
                self.ethnicity_data[mid] = None
                return None

            ethnicity = self.qid_to_ethnicity(qid)
            self.ethnicity_data[mid] = ethnicity

            return ethnicity
