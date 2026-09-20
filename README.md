# 🏠 HomeCare AI – Intelligent Home Maintenance Agent

> An AI-powered home maintenance management system that helps users track household assets, calculate maintenance schedules, identify upcoming or overdue tasks, and interact with an AI maintenance assistant.

---

## 👨‍💻 Developer

**Name:** Rohan Laharwani  
**PRN:** 24070521055  
**Course:** B.Tech Computer Science & Engineering  
**Specialization:** Artificial Intelligence & Machine Learning  

---

## 📌 Project Overview

**HomeCare AI** is an intelligent web-based home maintenance management application designed to simplify the tracking of household appliance maintenance.

Users can add household assets such as:

- Air Conditioners
- Refrigerators
- Washing Machines
- Water Purifiers
- Geysers
- Electrical Appliances
- Plumbing Equipment
- Other Household Assets

For every asset, the user provides the **last service date** and **maintenance interval**. The application automatically calculates the next service date and determines the current maintenance status.

The application also includes an **AI-powered maintenance assistant using the Groq API**, allowing users to ask questions about their maintenance schedule using natural language.

---

## ✨ Features

### 📊 Dashboard

The dashboard provides an overview of the home's maintenance condition.

It displays:

- Total Assets
- Overdue Maintenance
- Maintenance Due This Week
- Assets On Schedule
- Maintenance Overview
- Quick AI Assistant

---

### 🏠 Asset Management

Users can:

- Add new household assets
- Edit existing assets
- Delete assets
- Select asset categories
- Enter the last service date
- Select maintenance intervals
- View the next service date
- View the current maintenance status

---

### 📅 Automatic Maintenance Calculation

The application automatically calculates:

```text
Next Service Date =
Last Service Date + Maintenance Interval
