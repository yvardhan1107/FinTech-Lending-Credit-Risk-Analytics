-- PostgreSQL-compatible schema. Create tables, then import the generated CSVs.
CREATE TABLE customers (
 customer_id VARCHAR(20) PRIMARY KEY, registration_date DATE NOT NULL, age INT,
 gender VARCHAR(20), nationality_group VARCHAR(30), city VARCHAR(50),
 employment_status VARCHAR(30), employment_sector VARCHAR(30), employment_tenure_months INT,
 monthly_income NUMERIC(12,2), housing_status VARCHAR(30), dependents INT,
 customer_tenure_months INT, acquisition_channel VARCHAR(30), acquisition_campaign VARCHAR(60),
 customer_segment VARCHAR(40));
CREATE TABLE applications (
 application_id VARCHAR(30) PRIMARY KEY, customer_id VARCHAR(20) REFERENCES customers(customer_id),
 application_date DATE, requested_amount NUMERIC(12,2), requested_term_months INT,
 application_channel VARCHAR(30), acquisition_channel VARCHAR(30), credit_score INT,
 monthly_income_at_application NUMERIC(12,2), existing_debt NUMERIC(14,2), dti NUMERIC(8,4),
 previous_late_payments INT, previous_defaults INT, risk_score INT, risk_band VARCHAR(20),
 application_status VARCHAR(20), rejection_reason VARCHAR(80), underwriting_policy_version VARCHAR(20));
CREATE TABLE loans (
 loan_id VARCHAR(30) PRIMARY KEY, application_id VARCHAR(30) REFERENCES applications(application_id),
 customer_id VARCHAR(20) REFERENCES customers(customer_id), disbursement_date DATE,
 approved_amount NUMERIC(12,2), loan_term_months INT, annual_rate NUMERIC(8,4),
 monthly_payment NUMERIC(14,2), loan_type VARCHAR(30), risk_band VARCHAR(20),
 acquisition_channel VARCHAR(30), underwriting_policy_version VARCHAR(20),
 maturity_date DATE, loan_status VARCHAR(20));
CREATE TABLE repayments (
 repayment_id VARCHAR(30) PRIMARY KEY, loan_id VARCHAR(30) REFERENCES loans(loan_id),
 customer_id VARCHAR(20) REFERENCES customers(customer_id), due_date DATE, payment_date DATE,
 scheduled_payment NUMERIC(14,2), actual_payment NUMERIC(14,2), days_past_due INT,
 payment_status VARCHAR(20), missed_payment_flag INT, partial_payment_flag INT);
CREATE TABLE credit_risk_history (
 risk_assessment_id VARCHAR(30) PRIMARY KEY, customer_id VARCHAR(20) REFERENCES customers(customer_id),
 loan_id VARCHAR(30) REFERENCES loans(loan_id), assessment_date DATE, credit_score INT,
 risk_score INT, risk_band VARCHAR(20), dti NUMERIC(8,4), loan_to_income NUMERIC(10,3),
 previous_late_payments INT, previous_defaults INT, probability_of_default NUMERIC(8,4));
CREATE TABLE acquisition (
 acquisition_id VARCHAR(30) PRIMARY KEY, customer_id VARCHAR(20) REFERENCES customers(customer_id),
 acquisition_date DATE, acquisition_channel VARCHAR(30), campaign VARCHAR(60), partner VARCHAR(60),
 acquisition_cost NUMERIC(12,2), first_application_date DATE, converted_to_loan BOOLEAN);
CREATE TABLE collections (
 collection_id VARCHAR(30) PRIMARY KEY, loan_id VARCHAR(30) REFERENCES loans(loan_id),
 customer_id VARCHAR(20) REFERENCES customers(customer_id), collection_date DATE,
 days_past_due INT, collection_stage VARCHAR(30), contact_attempts INT,
 amount_recovered NUMERIC(14,2), recovery_cost NUMERIC(12,2), recovery_status VARCHAR(30));
CREATE TABLE monthly_business_kpis (
 month VARCHAR(7) PRIMARY KEY, applications INT, approvals INT, approval_rate NUMERIC(8,2),
 loans_disbursed INT, average_loan_size NUMERIC(14,2), total_disbursed NUMERIC(16,2),
 outstanding_portfolio NUMERIC(16,2), average_dti NUMERIC(8,4), delinquency_rate NUMERIC(8,2),
 default_rate NUMERIC(8,2), defaulted_loans INT, credit_loss NUMERIC(16,2),
 recovery_amount NUMERIC(16,2), revenue NUMERIC(16,2), acquisition_cost NUMERIC(16,2),
 operating_cost NUMERIC(16,2), funding_cost NUMERIC(16,2), profit NUMERIC(16,2), customer_count INT);
CREATE INDEX idx_app_customer ON applications(customer_id);
CREATE INDEX idx_app_date ON applications(application_date);
CREATE INDEX idx_loan_customer ON loans(customer_id);
CREATE INDEX idx_loan_date ON loans(disbursement_date);
CREATE INDEX idx_rep_loan ON repayments(loan_id);
CREATE INDEX idx_rep_due ON repayments(due_date);
CREATE INDEX idx_col_loan ON collections(loan_id);
CREATE INDEX idx_risk_loan ON credit_risk_history(loan_id);
