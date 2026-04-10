# BookOps
### COP4710 | Group 26 Database Final Project
A bookstore management system built with Python, Streamlit, and MySQL.

## Team Members
- Alejandro Gonzalez
- Andrew Puig
- Anncarolyne Power
- Lenyn Murillo Holguin

## Setup Instructions
### 0. Start MySQL 
Make sure the server is on and running. This project is hosted locally.

### 1. Load the database
```bash
mysql -u root -p < db_proof/schema.sql
mysql -u root -p < db_proof/data.sql
```

### 2. Install dependencies
```bash
pip3 install -r backend/requirements.txt
```

### 3. Configure your connection
Use `config.py` to fill in your MySQL credentials.

### 4. Run the app
```bash
cd frontend
python3 -m streamlit run app.py
```

---