import pandas as pd
from app.models.data_loader import DataLoader

class SummaryService:
    """
    Singleton class responsible for processing and summarizing legislative data
    Provides methods to generate summaries for legislators and bills
    """
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """
        Singleton implementation - ensures only one instance exists
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, data_loader=None):
        """
        Initialize SummaryService with DataLoader instance
        
        Args:
            data_loader (DataLoader, optional): DataLoader instance. Creates new one if None
        """
        # Prevent multiple initialization of the same instance
        if SummaryService._initialized:
            return
        
        # Initialize with provided DataLoader or create new singleton instance
        self.data_loader = data_loader or DataLoader()
        
        # Load initial data references
        self.refresh_data()
        
        # Mark as initialized
        SummaryService._initialized = True
    
    def refresh_data(self):
        """
        Refresh local data references from DataLoader
        Should be called after DataLoader loads new files
        """
        self.legislators = self.data_loader.legislators
        self.bills = self.data_loader.bills
        self.votes = self.data_loader.votes
        self.vote_results = self.data_loader.vote_results
    
    def get_legislators_summary(self):
        """
        Generate summary of legislators with their voting records
        
        Returns:
            pandas.DataFrame: DataFrame with columns [legislator_id, name, supported, opposed]
            None: If no data is available
        """
        # Check if all required data is available
        if (self.legislators.empty or self.bills.empty or 
            self.votes.empty or self.vote_results.empty):
            return None 
        
        # Group vote results by legislator and vote type, then count occurrences
        vote_counts = (
            self.vote_results
            .groupby(["legislator_id", "vote_type"])
            .size()
            .unstack(fill_value=0)
            .rename(columns={1: "supported", 2: "opposed"})
            .reset_index()
        )
        
        # Join vote counts with legislator information
        result = vote_counts.merge(
            self.legislators, 
            left_on="legislator_id",
            right_on="id"
        )
        
        # Return only relevant columns
        return result[["legislator_id", "name", "supported", "opposed"]]
    
    def get_bill_summary(self):
        """
        Generate summary of bills with support/opposition counts and primary sponsors
        
        Returns:
            pandas.DataFrame: DataFrame with columns [bill_id, title, supporters, opposers, primary_sponsor]
            None: If no data is available
        """
        # Check if all required data is available
        if (self.legislators.empty or self.bills.empty or 
            self.votes.empty or self.vote_results.empty):
            return None 
        
        # Join vote results with votes to get bill information
        merged = self.vote_results.merge(
            self.votes, 
            left_on="vote_id",
            right_on="id",
            suffixes=("_result", "_vote")   # Add suffixes to distinguish duplicate column names
        )
        
        # Group by bill and vote type, then count supporters/opposers
        vote_counts = (
            merged
            .groupby(["bill_id", "vote_type"])
            .size() # Count votes for each bill and vote type
            .unstack(fill_value=0) # Pivot vote_type to columns
            .rename(columns={1: "supporters", 2: "opposers"}) # Rename columns (1=yea, 2=nay)
            .reset_index() # Convert bill_id back to column
        )
        
        # Join bills with legislators to get sponsor information
        bills_with_sponsor = self.bills.merge(
            self.legislators,
            left_on="sponsor_id",
            right_on="id",
            how="left", # Keep all bills even if sponsor not found
            suffixes=('', '_sponsor')   # Add suffix to avoid column name conflicts
        )
        
        # Handle cases where sponsor is not found
        bills_with_sponsor["name"] = bills_with_sponsor["name"].fillna("Sponsor not found")
        
        # Join vote counts with bill and sponsor information
        result = vote_counts.merge(
            bills_with_sponsor,
            left_on="bill_id",
            right_on="id"
        )
        
        # Return only relevant columns and rename sponsor column for clarity
        return result[["bill_id", "title", "supporters", "opposers", "name"]].rename(
            columns={"name": "primary_sponsor"}
        )