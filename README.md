# multi-domain-intelligence-platform
# 🛡️ Multi-Domain Cyber Intelligence Platform  
### CST1510 — Week 8 to Week 10 Full Project

This repository contains the full implementation of my **Week 8, Week 9, and Week 10 coursework** for the Modular Multi-Domain Intelligence Platform.  
The system is divided into three main parts: a backend (Week 8), a Streamlit user interface (Week 9), and an optional API structure (Week 10). Each folder has a clear purpose in the architecture.

---

# 📁 Folder Structure Explained

This section explains **exactly what each folder holds** and **why it exists**.

---

## 📁 WEEK08_BACKEND — Backend + Database Layer

This folder contains the **core logic** of the entire system.

### 🔹 What this folder contains:

- **app/data/db.py**  
  Handles the SQLite connection.

- **app/data/schema.py**  
  Contains SQL code that creates all database tables:
  - users  
  - cyber_incidents  
  - datasets_metadata  
  - it_tickets  

- **app/data/incidents.py**  
  Functions for creating and retrieving cyber incidents.

- **app/data/users.py**  
  Functions for user management and authentication.

- **app/data/datasets.py**  
  Handles dataset metadata operations.

- **app/data/tickets.py**  
  Handles IT ticket operations.

- **app/services/user_service.py**  
  Full login + registration logic using hashing and validation.

- **DATA folder**  
  Holds:
  - All CSV files (which get loaded into the DB)
  - The final SQLite database: `intelligence_platform.db`

- **main.py**  
  Runs the entire Week 8 setup:
  - Creates tables  
  - Loads CSVs  
  - Maps CSV columns  
  - Tests authentication  
  - Inserts a sample incident  
  - Shows database summary  

### 🔹 Why this folder exists:
It is the **backbone** of the project.  
Week 9 UI and Week 10 API depend directly on this backend.

---

## 📁 WEEK09_STREAMLIT — Streamlit User Interface (Cyber Dashboard)

This is the **front-end** of the system.  
The UI connects directly to the Week 8 backend and displays data visually.

### 🔹 What this folder contains:

- **Home.py**  
  Login + Register page with session_state  
  Validates users using Week 8’s `users` table  
  Redirects to dashboard upon login  

- **app_backend/**  
  Light wrapper modules that connect Streamlit to Week 8 backend:
  - db.py → points to SQLite database  
  - users.py → login/register logic  
  - incidents.py → load + insert incidents  

- **pages/1_Dashboard.py**  
  The main cyber-themed dashboard with:
  - Filters (severity, status, date)
  - Incident severity chart
  - Time-series line chart
  - KPI metrics
  - Raw data table  
  All powered by real database data.

- **pages/2_Incidents.py**  
  Incident Management module:
  - View incident table  
  - Add a new incident  
  - Uses database insert + fetch functions  

### 🔹 Why this folder exists:
It provides a **visual SOC-style interface** for analysts to monitor incidents and interact with live data.

---

## 📁 WEEK10_API — API Architecture (Optional)

Even if not fully implemented, this folder outlines the API design planned for Week 10.

### 🔹 What this folder contains:
- Planned structure for a REST API (FastAPI recommended)
- Placeholder route files
- Notes describing how endpoints would connect backend ↔ UI

### 🔹 Why this folder exists:
Shows understanding of how the system can grow into a real-world architecture.

---

# 🔗 How All Folders Work Together

