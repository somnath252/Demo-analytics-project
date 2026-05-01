# RavenStack SaaS Analytics Portfolio Project

[![Live Demo](https://img.shields.io/badge/Live-View_Dashboard-success)](#) *(<-- Add your Streamlit Cloud link here!)*
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Data Stack](https://img.shields.io/badge/Stack-Pandas%20%7C%20Plotly%20%7C%20NumPy-lightgrey)](#)

This repository contains a portfolio-ready SaaS analytics implementation for RavenStack. It includes:

- `RavenStack_analysis.ipynb`: A Jupyter notebook for data loading, cleaning, feature engineering, and core analytics visualization.
- `saas_app.py`: A Streamlit executive dashboard for Revenue, Churn, and Product Usage analysis.
- `requirements.txt`: Python package dependencies for reproducibility.

## 🎯 The Business Case (Why I Built This)
In B2B SaaS, churn doesn't happen overnight—it happens slowly through product friction, unresolved support tickets, and feature underutilization. 

I built the **RavenStack Executive HQ** to demonstrate how to unify siloed data (CRM accounts, subscriptions, product telemetry, and support tickets) into a single, actionable narrative for GTM leaders. This project showcases my ability to turn raw data into strategic insights for Product Marketing, Growth, and RevOps teams.

---

## 📸 Dashboard Preview
*(Replace the placeholder below with a GIF or Screenshot of your Streamlit app)*

![RavenStack Dashboard Preview](https://via.placeholder.com/800x400.png?text=Add+a+Screenshot+or+GIF+of+your+Streamlit+App+Here)

---

## 🚀 Core Strategic Modules

### 1. 💰 Revenue & GTM Expansion
* **What it does:** Visualizes Monthly Recurring Revenue (MRR) distribution across Plan Tiers, Industries, and Geographies.
* **PMM Value:** Identifies our most lucrative Ideal Customer Profiles (ICPs). By mapping MRR to industry (via Sunburst charting), GTM teams can align ad spend and messaging toward the highest-LTV segments.

### 2. 📉 Churn Forensics
* **What it does:** Categorizes churn reasons and quantifies the financial impact (refunds/lost MRR) of each.
* **PMM Value:** Moves beyond qualitative feedback. By isolating churn reasons (e.g., "Missing Feature" vs "Pricing"), Product Marketing can adjust competitive battlecards and Product teams can prioritize the roadmap.

### 3. 🛠️ Product Friction Index
* **What it does:** Correlates feature adoption/usage counts against application error rates and median support ticket latency.
* **PMM Value:** High usage + high error rates = **Churn Risk**. This view allows Customer Success (CS) to proactively reach out to accounts experiencing friction before they cancel their renewal.

---

## 💻 Quick Start Guide

### Run the notebook
Open `RavenStack_analysis.ipynb` in Jupyter Notebook or VS Code. Execute each cell in order to see the step-by-step data cleaning, feature engineering (such as calculating the `friction_score`), and exploratory data analysis.

### Run the dashboard
If you'd like to spin up the interactive executive dashboard on your local machine, run the following commands in your terminal:

1. Install the required dependencies:
```bash
pip install -r requirements.txt

```
Launch the Streamlit app:
```bash
streamlit run saas_app.py

```
The dashboard will automatically open in your default web browser at http://localhost:8501.
###🧠 Technical Architecture & Data Hygiene
Behind the UI is a robust data cleaning pipeline that proves I understand data integrity:
* **Automated Type Casting:** Strict boolean casting and datetime parsing for reliable time-series analysis.
* **Metric Engineering:** Synthesized new KPIs on the fly, such as session_length_secs, friction_score, and ticket_latency_hours.
* **Relational Merging:** Safely joined 5 distinct relational datasets (Accounts, Subscriptions, Usage, Tickets, Churn) without data duplication or loss.

###🤝 Let's Connect
I built this project to demonstrate my ability to sit at the intersection of Data, Product, and Go-To-Market Strategy. If your SaaS company is looking for a professional who can translate raw database tables into revenue-driving narratives, let's talk.
Connect with me on LinkedIn | Send me an Email
