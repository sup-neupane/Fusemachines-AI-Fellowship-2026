import os
import logging
from constants import Environment
import argparse
from dotenv import load_dotenv #type:ignore

load_dotenv()

def setup_logging():
    logging.basicConfig(
        level = os.getenv("LOG_LEVEL", "INFO"),
        format = "%(asctime)s - %(levelname)s - %(message)s" 
    )

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description = "CLI Tool")
    parser.add_argument(
        "--env",
        type = str,
        required= True,
        choices= [e.value for e in Environment],
        help = "Traget Environment"
    )
    args = parser.parse_args()

    logging.info(f"Application initialized for {args.env} environments")

if __name__ == "__main__":
    main()