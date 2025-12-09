# 🛡️ Week 09 & 10 — Cyber Intelligence Platform (Streamlit + AI Assistant)

This project combines **Week 09** (Streamlit UI) and **Week 10** (AI Assistant Upgrade) into one full **Cyber Intelligence SOC Portal**.  
It connects to the Week 08 SQLite database, visualizes cyber data, and now includes a **smart AI chatbot** powered by **Google Gemini** to help users understand incidents, tickets, and datasets.

---

## 🎯 Project Objective Timeline

| Week | Focus | Result |
|------|-------|--------|
| **Week 09** | Build Streamlit UI with database connection | Fully functional SOC dashboard with forms, analytics, and multi-page structure |
| **Week 10** | Add an AI Chatbot using Gemini API | Smart SOC Assistant that can answer anything and interpret portal data |

---

## 🧬 Features Implemented

### 🔐 **1️⃣ Authentication System**
- Login & Register pages (tabs)
- Password hashing via backend
- Session state to keep users logged in
- Role support: `analyst` / `admin`
- Page access restrictions

---

### 📊 **2️⃣ Cyber-SOC Dashboard**
- Real incidents, tickets & dataset metrics
- KPI counters for overview
- **Charts:**
  - Incidents by severity
  - Tickets by status
  - Dataset sources (admin-only)
- Global map with SOC node locations
- Live threat-feed generator
- Network architecture graph (Graphviz)
- Animated hologram + radar scanner visuals

> UI styling fully customized with neon green **cyberpunk SOC theme**

---

### 🛡️ **3️⃣ Incident Management Page**
- **View all incidents** from database
- **Add new incident**
  - Date
  - Type
  - Severity
  - Status
  - Description
- Stored instantly in SQLite DB

---

### 🎫 **4️⃣ IT Ticket Overview**
- Displays all IT tickets
- Ticket metrics:
  - Open tickets count
  - High-priority tickets
- Visual analytics with bar charts

---

### 📚 **5️⃣ Dataset Metadata Page**
- Shows metadata table from DB
- Charts for:
  - Sources distribution
  - Record counts per dataset
- KPIs for datasets & total records

---

### 👤 **6️⃣ User Profile Page**
- Displays username + role
- Logout button resets session state

---

## 🤖 Week 10 Upgrade — AI SOC Assistant

A **Gemini-powered chatbot** that:
### 🧠 Understands the User
- Greets using **logged-in username**
- Friendly, balanced tone
- Remembers user interests during conversation

### 🔍 Uses Real SOC Data Intelligently
If the user asks about:
- incidents  
- severity  
- attacks  
- tickets  
- priority  
- datasets  

→ The AI **summarizes real values** from the database and explains them clearly  
(never makes up numbers)

### 🗣️ General Knowledge + Cyber Knowledge
- Can explain tech concepts  
- Can talk about music, life, gaming, business  
- Acts like a helpful, smart friend

---

## 🧠 Tech Stack

| Component | Technology |
|----------|------------|
| UI Framework | Streamlit |
| AI Assistant | Google Gemini API |
| Database | SQLite (from Week 08) |
| Data Processing | Pandas |
| Graphics | Graphviz, Streamlit Charts |
| Styling | Custom CSS (Neon Cyber Theme) |

---

## 📂 Project Structure

