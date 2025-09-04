
# AptEase - Conversational Apartment Finder

AptEase is a web application that allows users to search for apartments using natural language queries. The system translates user queries into SQL, fetches results from a SQLite database, and presents a summarized view for easy comparison.

## Demo
![AptEase-ConversationalApartmentFinder-GoogleChrome2025-07-1920-51-10-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/e08075ba-fee8-4e64-ac12-05eecbb76e8e)

## Features

- **Conversational Search:** Enter queries in plain English (e.g., "Show me 2-bedroom apartments in Berlin under $100/night").
- **Automatic SQL Generation:** Uses a fine-tuned T5 model to convert natural language to SQL.
- **Dynamic Results Table:** Sort, filter, and limit results interactively.
- **Summary Generation:** Summarizes top results and amenities for quick insights.
- **Modern UI:** Responsive, clean design with dull green theme.

## Project Structure

```
info project/
├── app.py                  # Flask backend
├── database.py             # SQLite DB setup and CSV import
├── text_to_sql.py          # T5 model for NL-to-SQL
├── generate_summary.py     # Summarizes results
├── templates/
│   └── index.html          # Main web UI
├── fine_tuned_model/       # Model files (excluded from git)
├── dataset_db/             # CSV datasets (excluded from git)
├── Pipfile                 # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Excludes large files
```

## Setup Instructions

1. **Clone the repository:**
	```bash
	git clone https://github.com/sijorejigeorge/AptEase.git
	cd AptEase/info\ project
	```

2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

3. **Run the application:**
	```bash
	python app.py
	```
	- Visit `http://localhost:5000` in your browser.

## Usage

- Enter a natural language query in the search box.
- View, sort, and filter results.
- Read the summary for quick insights.

## API Endpoints

- `/` : Main UI
- `/query` : Accepts POST requests with `{ "query": "..." }`, returns SQL and results.
- `/generate-summary` : Accepts POST requests with `{ "results": [...] }`, returns summary text.


## Requirements

- Python 3.7+
- Flask
- pandas
- transformers
- openai (if using OpenAI API)

All required datasets and model files are included in the repository. No manual download or placement is needed.


