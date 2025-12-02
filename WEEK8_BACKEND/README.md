# 🗂️ Week 08 — Multi-Domain Intelligence Platform (Backend + SQLite Database)

This folder contains the **Week 08 backend system**, which powers the Multi-Domain Intelligence Platform used later in Week 09’s Streamlit UI.

The goal of Week 08 is to build a **fully functional Python backend** that uses **SQLite** to store, retrieve, and manage data across multiple cybersecurity domains such as users, incidents, malware intel, threat intel, and activity logs.

This backend provides all the core functions required by the Week 09 interface, including authentication, incident storage, and analytics queries.

---

## 🎯 Key Objectives of Week 08

- Build a persistent **SQLite database**  
- Create the database schema for multiple intelligence tables  
- Implement **CRUD operations** (Create, Read, Update, Delete)  
- Develop Python functions to interact with the database  
- Enable the backend to integrate seamlessly with Streamlit in Week 09  
- Store real cyber incident and user account data  
- Use parameterized queries for **security against SQL injection**  

---

## 🛢️ Database Structure

The SQLite database contains the following primary tables:

### 👤 **1. users**
Stores all registered platform users.

Columns:
- `id`
- `username`
- `password_hash`
- `role`

### 🛡️ **2. cyber_incidents**
Stores cybersecurity incident data.

Columns:
- `id`
- `date`
- `type`
- `severity`
- `status`
- `description`

### 🧪 **3. malware_data**
Stores malware intelligence (optional or bonus).

Columns:
- malware name  
- threat level  
- signature  
- last seen  

### 🌐 **4. threat_intel**
Stores high-level threat intelligence indicators.

### 📜 **5. activity_log**
Captures actions performed by users (login, incident updates, etc.).

---

## 🧩 Backend Features Implemented

### 🔐 **1. User Authentication Backend**
- Secure password hashing  
- Register new users  
- Validate login credentials  
- Role support (admin/user)  

### 📝 **2. Incident Management Functions**
- Insert new incidents  
- Fetch all incidents  
- Filter incidents by severity, status, or date  
- Update or delete incidents  

### 🛢️ **3. Database Initialization Script**
The backend includes a setup method that:
- Creates the tables if they don’t exist  
- Ensures the database is ready for Week 09 UI  
- Uses safe, parameterized SQL commands  

### 🔗 **4. Reusable Database Connection Helper**
A clean helper method manages:
- Opening connections  
- Closing connections  
- Returning cursor objects  
- Handling errors safely  

---

## 📁 Folder Structure (Typical Week 08)

```
Week08_Backend/
│── app_backend/
│   ├── db.py                # Database connection + initialization
│   ├── users.py             # User authentication functions
│   ├── incidents.py         # Incident insertion + retrieval
│   ├── threats.py           # Threat intel functions (optional)
│   ├── logs.py              # Activity logging utilities
│
│── DATA/
│   └── intelligence_platform.db   # SQLite database file
│
└── main.py                   # Demo script for testing backend functions
```

---

## 🧪 How to Test the Backend

Run this command:

```bash
python main.py
```

Inside `main.py` you can test:
- User registration  
- Login validation  
- Adding incidents  
- Viewing database entries  

Everything from Week 09’s UI calls these backend functions.

---

## 🔮 What This Backend Enables in Week 09

This backend is 100% compatible with Week 09 and enables:

- Login & registration  
- SOC dashboard analytics  
- Adding/Viewing cyber incidents  
- Querying real stored data  
- Multi-page Streamlit UI integration  

---
