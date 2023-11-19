import os
from AgentQuery.modules.db import PostgressDb
import dotenv

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "DATABASE_URL not found"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def main():
    with 
    pass


if __name__ == "__main__":
    main()