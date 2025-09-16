# 🏋️‍♂️ Gym Membership Management System

A lightweight Gym Membership Management System built with **Python** and **SQLite3**. This system allows gym owners or admins to manage members, monitor activity, handle payments, and export reports to CSV.

---

## 📌 Features

✅ Add, remove, and edit gym members  
✅ Manage membership plans and durations  
✅ Automatically flag inactive members (based on check-ins)  
✅ Handle payment tracking and plan renewals  
✅ Log member check-ins  
✅ File complaints associated with members  
✅ Export data (e.g. member lists, payments) to `.csv`  
✅ Admin login system (basic authentication)  
✅ Built using Python’s built-in `sqlite3` module — no external DB required

---

## 🗂️ Project Structure

GymMembershipManagement/
├── src/
│   ├── main.py          # Entry point / menu system
│   ├── model.py         # Handles database interactions
│   ├── logic.py         # Business logic layer
│   └── db.py            # Data base initializer (e.g. CSV export)
├── gym.db               # SQLite3 database file (generated automatically)
├── README.md            # Project description
