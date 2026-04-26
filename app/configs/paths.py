import os

# PATHS AND DIRECTORIES
HOME_DIR = os.getcwd()
APP_DIR = os.path.join(HOME_DIR, "app")
LOCAL_STORAGE = os.path.join(APP_DIR, "local_storage")

TEMPLATE_PATH = os.path.join(APP_DIR, "configs", "prebuild-templates")

# templates paths
TEMPLATE_1 = os.path.join(TEMPLATE_PATH, "template_1.json")
TEMPLATE_2 = os.path.join(TEMPLATE_PATH, "2.json")
TEMPLATE_3 = os.path.join(TEMPLATE_PATH, "4.json")


# FILE NAMES
GOOGLE_SHEETS_NAME = "credentials_google_sheets.json"
GOOGLE_SHEETS_PATH = os.path.join(APP_DIR, "configs", "jsons", GOOGLE_SHEETS_NAME)

# keywords files
KW_LLMS_FILTERED_GKR = "kw_from_llms-gkr.xlsx"
KW_ARTICLES_FILTERED_GKR = "google_keyword_research.xlsx"


RESEARCHED_FILE = "research_file.json"
CRAWL_FOLDER_NAME = "crawl"
ARTICLE_FOLDER_NAME = "article"


def get_article_filename(mongo_id: str) -> str:
    ARTICLE_FILE = f"article-{mongo_id}.html"
    return ARTICLE_FILE


# def get_brand_folder(user_id):
#     USER_FOLDER = os.path.join(LOCAL_STORAGE, user_id)
#     CRAWLER_FOLDER = os.path.join(USER_FOLDER, "web_crawler")

#     os.makedirs(USER_FOLDER, exist_ok=True)
#     os.makedirs(CRAWLER_FOLDER, exist_ok=True)

#     crawl_file = "crawl.json"
#     summary_file = "data-bank.xlsx"

#     crawl_filepath = os.path.join(CRAWLER_FOLDER, crawl_file)
#     summary_filepath = os.path.join(CRAWLER_FOLDER, summary_file)

#     return USER_FOLDER, CRAWLER_FOLDER, crawl_filepath, summary_filepath


def get_brand_folder(brand_id):
    BRAND_FOLDER = os.path.join(LOCAL_STORAGE, brand_id)
    os.makedirs(BRAND_FOLDER, exist_ok=True)
    
    CRAWLER_FOLDER = os.path.join(BRAND_FOLDER, "web_crawler")
    os.makedirs(CRAWLER_FOLDER, exist_ok=True)

    crawl_file = "crawl.json"
    summary_file = "data-bank.json"

    crawl_filepath = os.path.join(CRAWLER_FOLDER, crawl_file)
    summary_filepath = os.path.join(CRAWLER_FOLDER, summary_file)

    return BRAND_FOLDER, CRAWLER_FOLDER, crawl_filepath, summary_filepath


def get_article_folder(brand_id,user_id, article_id):
    BRAND_FOLDER = os.path.join(LOCAL_STORAGE, brand_id)
    USER_FOLDER = os.path.join(BRAND_FOLDER, user_id)
    ARTICLE_FOLDER = os.path.join(USER_FOLDER, "articles", article_id)

    os.makedirs(USER_FOLDER, exist_ok=True)
    os.makedirs(ARTICLE_FOLDER, exist_ok=True)

    return USER_FOLDER, ARTICLE_FOLDER

# def get_article_db(brand_id,user_id,article_id):
#     pass