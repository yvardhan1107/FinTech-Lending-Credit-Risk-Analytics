
# Synthetic FinTech Lending Dataset

A synthetic dataset for practicing **FinTech analytics, banking, credit risk, and data analysis** using Python and SQL.

This project simulates the business operations of a fictional digital lending company in Saudi Arabia. It provides a learning environment for analysts, students, and data professionals to explore lending performance, borrower behavior, loan defaults, and financial risk.

> **Important:** This is a completely synthetic dataset. It does not contain real customer information, actual financial records, or confidential company data.

---

## 📌 Business Scenario

A fictional digital lending company operating in Saudi Arabia has experienced rapid growth in its loan portfolio. However, management has noticed an increase in credit risk and loan defaults.

The main business question is:

> **How can the company continue growing its lending portfolio while maintaining healthy credit risk and sustainable financial performance?**

This dataset allows you to investigate questions such as:

- Which customer segments have the highest default risk?
- Which factors are associated with loan defaults?
- Where is the financial impact of credit losses concentrated?
- How do previous late payments relate to defaults?
- Does the debt-to-income (DTI) ratio help differentiate risk?
- Does loan size relate to default risk?
- How do approval rates and loan volumes change over time?
- Did the April 2025 underwriting policy change affect portfolio performance?

---

## 📊 Dataset Overview

The dataset covers **January 2024 through December 2025** and contains interconnected tables representing different stages of the lending lifecycle.

### Business Flow

```text
Customer Acquisition
        ↓
Loan Application
        ↓
Credit Assessment
        ↓
Approval / Rejection
        ↓
Loan Disbursement
        ↓
Repayment
        ↓
Delinquency / Default
        ↓
Collections / Recovery
```

---

## 📁 Dataset Tables

### 1. `customers`

Contains customer-level information.

Example fields and attributes include:

- `customer_id`
- Demographic attributes
- Income information
- Employment information
- Risk characteristics
- Previous repayment behavior

### 2. `applications`

Contains loan application records.

Example fields and attributes include:

- `application_id`
- `customer_id`
- Application date
- Requested loan amount
- Debt-to-income ratio (DTI)
- Application status
- Rejection reason
- Customer acquisition information

### 3. `loans`

Contains approved and disbursed loan records.

Example fields include:

- `loan_id`
- `application_id`
- `customer_id`
- Approved loan amount
- Disbursement date
- Maturity date
- Loan status
- Risk band

Possible loan statuses include:

- Active
- Paid
- Defaulted
- Restructured
- Written Off

### 4. `repayments`

Contains loan repayment activity.

This table can be used to analyze:

- Repayment behavior
- Payment delays
- Outstanding balances
- Delinquency patterns
- Repayment performance

### 5. `credit_risk_history`

Contains historical credit-risk information.

Use this table to investigate changes in customer risk characteristics and their relationship with lending outcomes.

### 6. `acquisition`

Contains customer acquisition and marketing-channel information.

Useful for analyzing:

- Acquisition channels
- Customer quality
- Application volume
- Approval performance
- Channel-level credit risk

### 7. `collections`

Contains collections and recovery activity.

Useful for studying:

- Collection performance
- Recovery outcomes
- Default management
- Recovery rates

### 8. `monthly_business_kpis`

Contains monthly business-level KPI data.

Useful for analyzing trends in:

- Applications
- Approvals
- Loan disbursements
- Portfolio growth
- Defaults
- Credit risk

---

## 🔑 Primary Keys and Relationships

The main tables use identifiers such as:

| Table | Primary Key |
|---|---|
| Customers | `customer_id` |
| Applications | `application_id` |
| Loans | `loan_id` |

These relationships support end-to-end lending analysis.

### Simplified Relationship Structure

```text
customers
    │
    ├── applications
    │       │
    │       └── loans
    │             │
    │             ├── repayments
    │             └── collections
    │
    └── credit_risk_history
```

Refer to the actual CSV files and their column names when establishing database relationships.

---

## 🎯 Suggested Analytics Questions

### 1. Portfolio Performance

- How many loan applications are received each month?
- What is the loan approval rate?
- How many loans are disbursed?
- How is the loan portfolio growing over time?

### 2. Credit Risk Analysis

- What is the overall loan default rate?
- Which risk bands have the highest default rates?
- How does previous late-payment history relate to defaults?
- Does DTI help differentiate default risk?
- Does loan size relate to default risk?

### 3. Financial Impact Analysis

Do not focus only on default rates. Also investigate:

> **How much money is exposed to default?**

Consider analyzing:

- Default rate
- Defaulted loan amount
- Share of total defaulted loan amount
- Outstanding exposure
- Recovery amount and recovery rate, where supported by the available data

This helps distinguish between **the probability of risk** and **its financial impact**.

### 4. Customer Segmentation

Explore combinations such as:

```text
Risk Band
    +
Previous Late Payments
```

Or:

```text
Risk Band
    +
Debt-to-Income Ratio
    +
Loan Size
```

The objective is to identify customer segments that are both **high-risk and financially significant**.

### 5. Underwriting Policy Analysis

A simulated underwriting policy change is associated with **April 2025**.

Compare performance before and after the change:

```text
Before April 2025
        vs.
After April 2025
```

Investigate changes in:

- Approval rate
- Loan volume
- Average loan size
- Default rate
- Risk-band distribution
- Financial exposure

> **Note:** A change observed after the policy date does not automatically prove that the policy caused it. Consider other possible explanations and limitations in the data.

---

## 🛠️ Tools and Technologies

### Python

Recommended libraries:

```python
pandas
numpy
matplotlib
seaborn
```

Use Python for data cleaning, exploratory data analysis (EDA), segmentation, KPI calculations, and visualization.

### SQL

Load the CSV files into a database such as:

- PostgreSQL
- MySQL
- SQL Server
- SQLite
- DuckDB

Practice joins, aggregations, CTEs, window functions, subqueries, and business KPI calculations.

### Power BI

Build interactive dashboards to explore:

- Portfolio performance
- Credit risk
- Customer segmentation
- Default trends
- Financial exposure

### Excel

Practice:

- PivotTables
- Power Query
- XLOOKUP
- SUMIFS and COUNTIFS
- Charts
- KPI dashboards

---

## 📈 Suggested Analytics Framework

Follow a structured, business-focused approach:

```text
Business Problem
       ↓
KPI Baseline
       ↓
Customer Segmentation
       ↓
Risk Analysis
       ↓
Financial Impact
       ↓
Root-Cause Investigation
       ↓
Business Recommendations
```

A strong analysis should answer:

- **WHO** is affected?
- **WHAT** is happening?
- **WHEN** did it happen?
- **WHY** might it be happening?
- **WHAT** is the financial impact?
- **WHAT** should management do?

---

## ⚠️ Data Notes and Limitations

This dataset is designed for **learning and analytical practice**.

- It does not represent the actual Saudi lending market or the operations of a real financial institution.
- Some patterns and business events may be intentionally included to create analytical questions.
- The dataset should be treated as a simulation, not as real-world financial evidence.
- Validate data quality, missing values, duplicate records, date ranges, and relationships before drawing conclusions.
- Confirm column names and table relationships against the actual files before writing queries.

---

## 🚀 How to Use This Repository

Clone the original dataset repository:

```bash
git clone https://github.com/yvardhan1107/FinTech-Lending-Credit-Risk-Analytics
```

Move into the repository directory:

```bash
cd namaa-finance-synthetic-dataset
```

Locate the CSV files and begin your analysis using your preferred tools.

### Recommended Workflow

1. Data profiling
2. Data-quality checks
3. KPI calculation
4. Customer segmentation
5. Credit-risk analysis
6. Financial-impact analysis
7. Visualization
8. Business recommendations

---

## 🤝 For Learners

If you are learning **Data Analytics, FinTech, Banking Analytics, Credit Risk, Python, SQL, or Power BI**, you can use this dataset to practice and develop projects such as:

- Data analytics portfolio projects
- SQL business-analysis exercises
- Python EDA notebooks
- Power BI dashboards
- Credit-risk analysis
- Business case-study presentations
- Interview preparation projects

If you create an interesting analysis using this dataset, consider sharing your findings and documenting your methodology.

---

## 👤 About

**Maintained by Yashvardhan Agarwal**

This project focuses on practicing:

**Data Analytics → FinTech → Credit Risk → Business Insights**

The objective is to solve business problems using data analysis, Python, SQL, and data-driven recommendations.

The underlying dataset is attributed to its original creator. If you redistribute it, retain appropriate attribution to the original source.

---

⭐ If you find this project useful, consider starring the repository and sharing your analysis.

**Happy analyzing!**
