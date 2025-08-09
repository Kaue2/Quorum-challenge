import pandas as pd
from app.models.data_loader import DataLoader

class SummaryService:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, data_loader=None):
        # Evita reinicialização múltipla
        if SummaryService._initialized:
            return
            
        self.data_loader = data_loader or DataLoader()
        self.refresh_data()
        SummaryService._initialized = True
    
    def refresh_data(self):
        self.legislators = self.data_loader.legislators
        self.bills = self.data_loader.bills
        self.votes = self.data_loader.votes
        self.vote_results = self.data_loader.vote_results
    
    def get_legislators_summary(self):
        if (self.legislators.empty or self.bills.empty or 
            self.votes.empty or self.vote_results.empty):
            return None 
        
        vote_counts = (
            self.vote_results
            .groupby(["legislator_id", "vote_type"])
            .size()
            .unstack(fill_value=0)
            .rename(columns={1: "supported", 2: "opposed"})
            .reset_index()
        )
        
        result = vote_counts.merge(
            self.legislators, 
            left_on="legislator_id",
            right_on="id"
        )
        
        return result[["legislator_id", "name", "supported", "opposed"]]
    
    def get_bill_summary(self):
        if (self.legislators.empty or self.bills.empty or 
            self.votes.empty or self.vote_results.empty):
            return None 
        
        merged = self.vote_results.merge(
            self.votes, 
            left_on="vote_id",
            right_on="id",
            suffixes=("_result", "_vote")
        )
        
        vote_counts = (
            merged
            .groupby(["bill_id", "vote_type"])
            .size()
            .unstack(fill_value=0)
            .rename(columns={1: "supporters", 2: "opposers"})
            .reset_index()
        )
        
        bills_with_sponsor = self.bills.merge(
            self.legislators,
            left_on="sponsor_id",
            right_on="id",
            how="left",
            suffixes=('', '_sponsor')
        )
        
        bills_with_sponsor["name"] = bills_with_sponsor["name"].fillna("Sponsor not found")
        
        result = vote_counts.merge(
            bills_with_sponsor,
            left_on="bill_id",
            right_on="id"
        )
        
        return result[["bill_id", "title", "supporters", "opposers", "name"]].rename(
            columns={"name": "primary_sponsor"}
        )