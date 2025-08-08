from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CSV_PATHS = {
    "legislators": BASE_DIR / "data/legislators_(2).csv",
    "bills": BASE_DIR / "data/bills_(2).csv",
    "votes": BASE_DIR / "data/votes_(2).csv",
    "vote_results": BASE_DIR / "data/vote_results_(2).csv"
}