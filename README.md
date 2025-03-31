## Prerequisites

- Python 3.x
- Poetry (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/document-extraction.git
cd document-extraction
```

2. Install dependencies using Poetry:
```bash
poetry install
```

If you encounter any warnings about the project not being installable, you can safely ignore them as the project is configured in non-package mode.

3. configure .env

## Running the Application

To run the application, execute:

```bash
poetry run python main.py sample.pdf
```