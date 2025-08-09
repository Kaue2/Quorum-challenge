import pandas as pd
from app.utils.paths import CSV_PATHS
import os

class DataLoader:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if DataLoader._initialized:
            return
        
        self.legislators = pd.DataFrame()
        self.bills = pd.DataFrame()
        self.votes = pd.DataFrame()
        self.vote_results = pd.DataFrame()
        DataLoader._initialized = True
        
    def load_files(self, csv_paths=None):
        paths = csv_paths or CSV_PATHS
        if (os.path.exists(CSV_PATHS["legislators"]) and
            os.path.exists(CSV_PATHS["bills"]) and
            os.path.exists(CSV_PATHS["votes"]) and
            os.path.exists(CSV_PATHS["vote_results"])):
            
            self.legislators = pd.read_csv(CSV_PATHS["legislators"])
            self.bills = pd.read_csv(CSV_PATHS["bills"])
            self.votes = pd.read_csv(CSV_PATHS["votes"])
            self.vote_results = pd.read_csv(CSV_PATHS["vote_results"])
        else:
            pass
