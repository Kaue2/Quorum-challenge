import pandas as pd
from app.utils.paths import CSV_PATHS
import os

class DataLoader:
    """
    Singleton class responsible for loading and managing CSV data
    Ensures only one instance exists throughout the application lifecycle
    """
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """
        Singleton implementation - creates only one instance of DataLoader
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize DataLoader with empty DataFrames
        Uses _initialized flag to prevent multiple initializations
        """
        # Prevent multiple initialization of the same instance
        if DataLoader._initialized:
            return
        
        # Initialize empty DataFrames for each data type
        self.legislators = pd.DataFrame()
        self.bills = pd.DataFrame()
        self.votes = pd.DataFrame()
        self.vote_results = pd.DataFrame()
        
        # Mark as initialized
        DataLoader._initialized = True
        
    def load_files(self, csv_paths=None):
        """
        Load CSV files into DataFrames
        
        Args:
            csv_paths (dict, optional): Dictionary with file paths. Uses CSV_PATHS if None
        """
        # Use provided paths or default CSV_PATHS
        paths = csv_paths or CSV_PATHS
        
        # Check if all required CSV files exist
        if (os.path.exists(CSV_PATHS["legislators"]) and
            os.path.exists(CSV_PATHS["bills"]) and
            os.path.exists(CSV_PATHS["votes"]) and
            os.path.exists(CSV_PATHS["vote_results"])):
            
            # Load each CSV file into corresponding DataFrame
            self.legislators = pd.read_csv(CSV_PATHS["legislators"])
            self.bills = pd.read_csv(CSV_PATHS["bills"])
            self.votes = pd.read_csv(CSV_PATHS["votes"])
            self.vote_results = pd.read_csv(CSV_PATHS["vote_results"])
        else:
            # If files don't exist, keep DataFrames empty
            pass
