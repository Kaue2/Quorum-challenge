from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CSV_PATHS = {
    "legislators": BASE_DIR / "upload/legislators.csv",
    "bills": BASE_DIR / "upload/bills.csv",
    "votes": BASE_DIR / "upload/votes.csv",
    "vote_results": BASE_DIR / "upload/vote_results.csv"
}