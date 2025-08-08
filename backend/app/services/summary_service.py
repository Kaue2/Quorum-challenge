import pandas as pd

class SummaryService:
    def __init__(self, data_loader):
        self.legislators = data_loader.legislators
        self.bills = data_loader.bills
        self.votes = data_loader.votes
        self.vote_results = data_loader.vote_results
    
    def get_legislators_summary(self):
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
    
    def get_bill_summary(self):  #
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
        
        bills_with_sponsor["name"] = bills_with_sponsor["name"].fillna("Patrocinador não encontrado")
        
        result = vote_counts.merge(
            bills_with_sponsor,
            left_on="bill_id",
            right_on="id"
        )
        
        return result[["bill_id", "title", "supporters", "opposers", "name"]].rename(
            columns={"name": "primary_sponsor"}
        )