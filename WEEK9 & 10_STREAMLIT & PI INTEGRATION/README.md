# 🛡️ Week 09 — Cyber Intelligence Platform (Streamlit UI)

This folder contains the **Week 09 Streamlit-based graphical interface** for the Multi-Domain Intelligence Platform.  

The goal of this week is to build a functional user interface that connects directly to the **Week 08 SQLite database**, uses real incident data, and demonstrates interactive visual analytics using Streamlit.

To make the interface more engaging and realistic for a cybersecurity environment, I implemented a **modern cyber-SOC themed UI** (dark mode + neon green), while still following all workshop requirements such as:

- session state  
- login + register  
- multiple Streamlit pages  
- charts, tables, filters, forms  
- widgets shown in the workshop templates  
- multi-page routing structure and sidebar usage  

Every advanced feature is built *on top of* the same techniques demonstrated in the workshop sessions.

---

## 🎯 Key Features Implemented This Week

### 🔐 **1. Full Authentication System**
- Login and Register pages using tabs  
- Password verification via Week 08 backend  
- Session handling with `st.session_state`  
- Access restriction for secured pages  

### 🧬 **2. Cyber-Themed SOC Dashboard**
- Real data from Week 08 (`cyber_incidents` table)  
- Severity breakdown bar chart  
- Time-series line graph of incidents  
- KPI metrics (total incidents, open cases, high severity)  
- Complex interactive filters:  
  - Severity  
  - Status  
  - Date range  
- Raw data table using `st.dataframe()`  
- Styling using injected CSS for a neon green hacker feel  

### 📝 **3. Incident Management**
- “View Incidents” tab showing all incidents from DB  
- “Add New Incident” form:  
  - Date  
  - Type  
  - Severity  
  - Status  
  - Description  
- Automatically linked to Week 08’s `insert_incident()`  
- Auto-refresh after insertion  

### 🗂️ **4. Multi-Page Structure**
This app uses Streamlit’s built-in multi-page system with separate pages for:
- Dashboard  
- Incident Management  
- User Authentication  
- Settings / Profile  
