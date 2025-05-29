import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def process_category_files(output_file: str = "data/users.csv") -> bool:
    """
    Process category CSV files and combine them into a single users.csv file
    """
    try:
        # Category mappings
        category_files = {
            "fashion": "category/پیج-لباس 25 - dataset_instagram-scraper_2025-05-28_08-31-49-556.csv",
            "home_decor": "category/لوازم خانگی 100 - dataset_instagram-scraper_2025-05-28_08-49-29-232.csv",
            "cosmetics": "category/محصولات بهداشتی 100 - dataset_instagram-scraper_2025-05-28_08-39-56-760 (1).csv"
        }

        # Initialize an empty list to store all users
        all_users = []

        # Process each category file
        for category, file_path in category_files.items():
            try:
                df = pd.read_csv(file_path)
                
                # Select only required columns and rename them
                df = df[["username", "followersCount"]]
                
                # Add category and status columns
                df["category"] = category
                df["status"] = "pending"
                
                # Append to our list
                all_users.append(df)
                logger.info(f"Processed {file_path} with {len(df)} users")

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
                continue

        if not all_users:
            logger.error("No data was processed from any file")
            return False

        # Combine all dataframes
        final_df = pd.concat(all_users, ignore_index=True)

        # Sort by followers count (descending)
        final_df = final_df.sort_values("followersCount", ascending=False)

        # Save to users.csv
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True)
        
        # Select and reorder columns for final output
        final_df = final_df[["username", "category", "status", "followersCount"]]
        final_df.to_csv(output_file, index=False)

        logger.info(f"Successfully created {output_file} with {len(final_df)} users")
        return True

    except Exception as e:
        logger.error(f"Error in process_category_files: {str(e)}")
        return False

if __name__ == "__main__":
    # Setup basic logging
    logging.basicConfig(level=logging.INFO)
    process_category_files() 