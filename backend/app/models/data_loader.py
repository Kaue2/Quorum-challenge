import pandas as pd
from app.utils.paths import CSV_PATHS

class DataLoader:
    def __init__(self):
        self.legislators = pd.read_csv(CSV_PATHS["legislators"])
        self.bills = pd.read_csv(CSV_PATHS["bills"])
        self.votes = pd.read_csv(CSV_PATHS["votes"])
        self.vote_results = pd.read_csv(CSV_PATHS["vote_results"])
