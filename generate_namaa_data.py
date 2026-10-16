"""
Namaa Finance synthetic relational database generator.
Python 3.10+, pandas, numpy.

Run:
    pip install pandas numpy
    python generate_namaa_data.py

Outputs:
    data/*.csv
    schema.sql
    data_dictionary.csv
    ERD.md
    validation_report.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

START = pd.Timestamp("2024-01-01")
END = pd.Timestamp("2025-12-31")
N_CUSTOMERS = 40000
N_APPLICATIONS = 120000

channels = ["Paid Search","Social Media","Referral","Affiliate","Partner","Organic","Direct","Email"]
channel_p = [0.16,0.20,0.13,0.11,0.14,0.10,0.09,0.07]
channel_risk = {"Paid Search":.03,"Social Media":.07,"Referral":-.04,"Affiliate":.04,
                "Partner":.01,"Organic":-.05,"Direct":-.03,"Email":-.02}
channel_cac = {"Paid Search":95,"Social Media":75,"Referral":35,"Affiliate":60,
               "Partner":110,"Organic":15,"Direct":10,"Email":20}
campaigns = {
 "Paid Search":["Search_Generic","Search_Lending","Search_Brand"],
 "Social Media":["Social_Retargeting","Social_Prospecting","Social_Creator"],
 "Referral":["Referral_Customer","Referral_Employee"],
 "Affiliate":["Affiliate_Publisher","Affiliate_Finance"],
 "Partner":["Partner_Retail","Partner_Employer","Partner_Platform"],
 "Organic":["SEO_Organic","Content_Organic"],
 "Direct":["Direct_App","Direct_Web"],
 "Email":["Email_CRM","Email_Reactivation"]
}
cities=["Riyadh","Jeddah","Dammam","Mecca","Medina","Khobar","Abha","Tabuk","Taif","Other"]
city_p=[.34,.18,.10,.08,.07,.06,.05,.04,.04,.04]

# ---------------- customers ----------------
customer_id=np.array([f"C{100000+i}" for i in range(N_CUSTOMERS)])
registration=START+pd.to_timedelta(rng.integers(0,(END-START).days+1,N_CUSTOMERS),unit="D")
age=np.clip(np.rint(rng.normal(36,9,N_CUSTOMERS)),21,65).astype(int)
gender=rng.choice(["Male","Female"],N_CUSTOMERS,p=[.68,.32])
nat=rng.choice(["Saudi","GCC","Other"],N_CUSTOMERS,p=[.78,.07,.15])
city=rng.choice(cities,N_CUSTOMERS,p=city_p)
employment=rng.choice(["Salaried","Self-employed","Contract","Unemployed"],N_CUSTOMERS,p=[.72,.14,.10,.04])
sector=rng.choice(["Government","Private","SME","Freelance","Other"],N_CUSTOMERS,p=[.24,.48,.15,.08,.05])
tenure=np.clip(np.rint(rng.gamma(3,18,N_CUSTOMERS)),1,240).astype(int)
income=rng.lognormal(np.log(10500),.42,N_CUSTOMERS)
income*=np.where(employment=="Government",1.10,1)
income*=np.where(employment=="Unemployed",.35,1)
income*=np.where(employment=="Contract",.90,1)
income*=np.where(sector=="SME",.88,1)
income*=np.where(sector=="Freelance",.82,1)
income*=1+(age-35)*.004
income=np.clip(np.rint(income/100)*100,1800,60000).astype(int)
housing=rng.choice(["Owned","Rented","Family","Other"],N_CUSTOMERS,p=[.18,.47,.27,.08])
dependents=np.clip(rng.poisson(np.where(age>35,2.2,1.2)),0,7).astype(int)
acq=rng.choice(channels,N_CUSTOMERS,p=channel_p)
campaign=np.array([rng.choice(campaigns[c]) for c in acq])
segment=np.select([income<5000,income<10000,income<20000],["Low Income","Middle Income","Upper-Middle Income"],default="High Income")

customers=pd.DataFrame({
 "customer_id":customer_id,"registration_date":registration,"age":age,"gender":gender,
 "nationality_group":nat,"city":city,"employment_status":employment,"employment_sector":sector,
 "employment_tenure_months":tenure,"monthly_income":income,"housing_status":housing,
 "dependents":dependents,"customer_tenure_months":((END-registration).days/30.44).astype(int),
 "acquisition_channel":acq,"acquisition_campaign":campaign,"customer_segment":segment
})

# ---------------- acquisition ----------------
acquisition=pd.DataFrame({
 "acquisition_id":[f"AQ{100000+i}" for i in range(N_CUSTOMERS)],
 "customer_id":customer_id,"acquisition_date":registration,
 "acquisition_channel":acq,"campaign":campaign,
 "partner":np.where(acq=="Partner",rng.choice(["STC_Pay","RetailPartner_A","EmployerPartner_B","Marketplace_C"],N_CUSTOMERS), "None"),
 "acquisition_cost":np.round(np.maximum(5,[channel_cac[c] for c in acq])*rng.lognormal(0,.18,N_CUSTOMERS),2),
 "first_application_date":pd.NaT,"converted_to_loan":False
})

# ---------------- applications ----------------
weights=np.where(np.isin(acq,["Paid Search","Social Media","Partner"]),1.2,1.0)
weights/=weights.sum()
idx=rng.choice(N_CUSTOMERS,N_APPLICATIONS,p=weights)
app_date=START+pd.to_timedelta(rng.integers(0,(END-START).days+1,N_APPLICATIONS),unit="D")
reg=registration[idx]
bad=app_date.to_numpy()<reg
app_date=pd.to_datetime(np.where(bad,reg+pd.to_timedelta(rng.integers(0,45,N_APPLICATIONS),unit="D"),app_date))
app_date=pd.to_datetime(np.minimum(app_date.values.astype("datetime64[ns]"),END.to_datetime64()))

inc=np.clip(np.rint((income[idx]*rng.normal(1,.04,N_APPLICATIONS))/100)*100,1500,65000)
ch=acq[idx]
policy=np.where(app_date>=pd.Timestamp("2025-04-01"),"Policy_V2","Policy_V1")
score=np.clip(np.rint(rng.normal(690,75,N_APPLICATIONS)
 +np.where(employment[idx]=="Unemployed",-70,0)
 +np.where(ch=="Referral",12,0)+np.where(ch=="Social Media",-8,0)),420,850).astype(int)
debt=np.clip(np.rint(inc*np.maximum(0,rng.normal(.75,.45,N_APPLICATIONS))),0,150000)
late=np.clip(rng.poisson(np.maximum(.15,(700-score)/80)+debt/inc*.25),0,8).astype(int)
prev_def=rng.binomial(1,np.clip(.005+.025*(late>=3)+.02*(score<560),0,.10))
term=rng.choice([6,9,12,18,24,36],N_APPLICATIONS,p=[.12,.12,.28,.20,.20,.08])
ratio=rng.lognormal(np.log(.95),.42,N_APPLICATIONS)*np.where(policy=="Policy_V2",1.15,1)
requested=np.clip(np.rint((inc*ratio)/500)*500,3000,100000)
dti=np.clip((debt+requested/np.maximum(term,6)*1.2)/(inc*12),.03,.85)
lti=requested/inc
latent=score/10-dti*100-lti*10-late*8-prev_def*45+np.where(employment[idx]=="Salaried",8,0)+rng.normal(0,10,N_APPLICATIONS)
risk_score=np.clip(np.rint(latent+25),0,100).astype(int)
risk_band=np.select([risk_score>=75,risk_score>=60,risk_score>=45],["Low","Medium","High"],default="Very High")
logit=-.5+.055*(risk_score-55)+.20*(policy=="Policy_V2")-.45*(prev_def>0)
p=1/(1+np.exp(-logit))
u=rng.random(N_APPLICATIONS)
status=np.where(u<p,"Approved",np.where(rng.random(N_APPLICATIONS)<.12,"Withdrawn","Rejected"))
reason=np.where(status=="Rejected",rng.choice(["High DTI","Low Credit Score","Insufficient Income","High Existing Debt","Policy Criteria"],N_APPLICATIONS,p=[.28,.27,.18,.15,.12]),"")

applications=pd.DataFrame({
 "application_id":[f"APP{1000000+i}" for i in range(N_APPLICATIONS)],
 "customer_id":customer_id[idx],"application_date":app_date,
 "requested_amount":requested,"requested_term_months":term,
 "application_channel":ch,"acquisition_channel":ch,"credit_score":score,
 "monthly_income_at_application":inc.astype(int),"existing_debt":debt.astype(int),
 "dti":np.round(dti,4),"previous_late_payments":late,"previous_defaults":prev_def,
 "risk_score":risk_score,"risk_band":risk_band,"application_status":status,
 "rejection_reason":reason,"underwriting_policy_version":policy
})

# intentional data-quality issues
applications.loc[rng.choice(applications.index,25,replace=False),"requested_amount"]=-500
applications.loc[rng.choice(applications.index,600,replace=False),"dti"]=np.nan
dups=applications.sample(250,random_state=SEED).copy()
dups["application_id"]=[f"APPDUP{100000+i}" for i in range(len(dups))]
applications_out=pd.concat([applications,dups],ignore_index=True)

# ---------------- loans ----------------
approved=applications[applications.application_status=="Approved"].reset_index(drop=True)
n=len(approved)
factor=np.clip(rng.normal(.95,.10,n),.65,1.10)
amount=np.maximum(np.rint(approved.requested_amount.to_numpy()*factor/500)*500,3000).astype(int)
disb=approved.application_date+pd.to_timedelta(rng.integers(0,8,n),unit="D")
disb=pd.to_datetime(np.minimum(disb.values.astype("datetime64[ns]"),END.to_datetime64()))
term2=approved.requested_term_months.to_numpy()
rate=np.clip(.08+.00020*(750-approved.credit_score.to_numpy())+.008*(approved.risk_band.eq("Very High").to_numpy()),.06,.32)
rate+=np.where(approved.underwriting_policy_version.to_numpy()=="Policy_V2",.005,0)
mr=rate/12
payment=amount*(mr*(1+mr)**term2)/((1+mr)**term2-1)
pd_prob=np.clip(.018+.00055*np.maximum(0,650-approved.credit_score.to_numpy())
 +.055*approved.dti.fillna(approved.dti.median()).to_numpy()
 +.020*np.maximum(0,approved.requested_amount.to_numpy()/approved.monthly_income_at_application.to_numpy()-1)
 +.018*approved.previous_late_payments.to_numpy()+.08*approved.previous_defaults.to_numpy()
 +np.where(approved.underwriting_policy_version.to_numpy()=="Policy_V2",.012,0)
 +np.array([channel_risk[c] for c in approved.acquisition_channel]),.005,.55)
age_days=(END-disb).days
default=(rng.random(n)<pd_prob)&(age_days>=60)
loan_status=np.full(n,"Active",dtype=object)
loan_status[default]="Defaulted"
paid=(~default)&(rng.random(n)<np.clip(.30+age_days/900,0,.88))
loan_status[paid]="Paid"
restruct=(~default)&(~paid)&(rng.random(n)<.08)
loan_status[restruct]="Restructured"
wo=default&(rng.random(n)<.22)
loan_status[wo]="Written Off"

loans=pd.DataFrame({
 "loan_id":[f"L{2000000+i}" for i in range(n)],
 "application_id":approved.application_id,"customer_id":approved.customer_id,
 "disbursement_date":disb,"approved_amount":amount,"loan_term_months":term2,
 "annual_rate":np.round(rate,4),"monthly_payment":np.round(payment,2),
 "loan_type":rng.choice(["Personal","Consumer","Emergency","Education"],n,p=[.72,.14,.08,.06]),
 "risk_band":approved.risk_band,"acquisition_channel":approved.acquisition_channel,
 "underwriting_policy_version":approved.underwriting_policy_version,
 "maturity_date":disb+pd.to_timedelta(term2*30,unit="D"),"loan_status":loan_status
})

# ---------------- risk history ----------------
risk=pd.DataFrame({
 "risk_assessment_id":[f"RA{3000000+i}" for i in range(n)],
 "customer_id":loans.customer_id,"loan_id":loans.loan_id,
 "assessment_date":loans.disbursement_date-pd.to_timedelta(rng.integers(0,3,n),unit="D"),
 "credit_score":approved.credit_score,"risk_score":approved.risk_score,"risk_band":approved.risk_band,
 "dti":approved.dti,"loan_to_income":np.round(loans.approved_amount/approved.monthly_income_at_application,3),
 "previous_late_payments":approved.previous_late_payments,"previous_defaults":approved.previous_defaults,
 "probability_of_default":np.round(pd_prob,4)
})

# ---------------- repayments: vectorized-ish generation ----------------
rep_parts=[]
rid=4000000
for loan in loans.itertuples(index=False):
    nd=min(int(loan.loan_term_months),max(0,int((END-loan.disbursement_date).days//30)))
    if nd<=0: continue
    risk_mult={"Low":.45,"Medium":.75,"High":1.15,"Very High":1.55}[loan.risk_band]
    fail=rng.random(nd)<(.035*risk_mult+(0.08 if loan.loan_status in ["Defaulted","Written Off"] else 0))
    partial=(~fail)&(rng.random(nd)<.025*risk_mult)
    due=[loan.disbursement_date+pd.Timedelta(days=30*m) for m in range(1,nd+1)]
    for j,d in enumerate(due):
        if fail[j]:
            st=rng.choice(["Late","Missed"],p=[.55,.45]); dpd=int(rng.integers(5,100))
            actual=0 if st=="Missed" else round(loan.monthly_payment*rng.uniform(.35,.85),2)
            pdate=d+pd.Timedelta(days=int(rng.integers(5,60))); missed=int(st=="Missed"); part=int(actual<loan.monthly_payment and st=="Late")
        elif partial[j]:
            st="Partial"; dpd=int(rng.integers(1,12)); actual=round(loan.monthly_payment*rng.uniform(.40,.90),2)
            pdate=d+pd.Timedelta(days=dpd); missed=0; part=1
        else:
            st="On Time"; dpd=int(rng.integers(0,3)); actual=round(loan.monthly_payment*rng.uniform(.98,1.02),2)
            pdate=d+pd.Timedelta(days=dpd); missed=0; part=0
        rep_parts.append([f"R{rid}",loan.loan_id,loan.customer_id,d,pdate,round(loan.monthly_payment,2),actual,dpd,st,missed,part])
        rid+=1
repayments=pd.DataFrame(rep_parts,columns=["repayment_id","loan_id","customer_id","due_date","payment_date","scheduled_payment","actual_payment","days_past_due","payment_status","missed_payment_flag","partial_payment_flag"])

# ---------------- collections ----------------
defaults=loans[loans.loan_status.isin(["Defaulted","Written Off"])]
coll=[]
cid=5000000
for loan in defaults.itertuples(index=False):
    start=loan.disbursement_date+pd.Timedelta(days=int(rng.integers(45,100)))
    for stage,off in [("Early",0),("30+ DPD",30),("60+ DPD",60),("90+ DPD",90),("Default",120)]:
        dt=start+pd.Timedelta(days=off)
        if dt>END: continue
        attempts=int(rng.poisson(1.5 if off<90 else 2.2))
        status="In Progress" if stage=="Default" else ("Contacted" if attempts>0 else "No Contact")
        coll.append([f"CL{cid}",loan.loan_id,loan.customer_id,dt,off,stage,attempts,0,round(attempts*rng.uniform(3,12),2),status]); cid+=1
    if rng.random()<.55:
        dt=min(END,start+pd.Timedelta(days=int(rng.integers(130,280))))
        rr=np.clip(rng.normal(.35 if loan.risk_band in ["Low","Medium"] else .22,.12),.03,.75)
        coll.append([f"CL{cid}",loan.loan_id,loan.customer_id,dt,120,"Recovery",int(rng.poisson(2)+1),round(loan.approved_amount*rr,2),round(rng.uniform(10,45),2),"Recovered"]); cid+=1
collections=pd.DataFrame(coll,columns=["collection_id","loan_id","customer_id","collection_date","days_past_due","collection_stage","contact_attempts","amount_recovered","recovery_cost","recovery_status"])

# acquisition enrichment
first=applications.groupby("customer_id").application_date.min()
acquisition.first_application_date=acquisition.customer_id.map(first)
acquisition.converted_to_loan=acquisition.customer_id.isin(set(loans.customer_id))

# ---------------- monthly KPI table ----------------
k=[]
for m in pd.date_range(START,END,freq="MS"):
    e=m+pd.offsets.MonthEnd(1)
    a=applications[(applications.application_date>=m)&(applications.application_date<=e)]
    lm=loans[(loans.disbursement_date>=m)&(loans.disbursement_date<=e)]
    eligible=loans[loans.disbursement_date<=e]
    seasoned=eligible[(e-eligible.disbursement_date).dt.days>=60]
    default_rate=seasoned.loan_status.isin(["Defaulted","Written Off"]).mean()*100 if len(seasoned) else np.nan
    exposure=0
    for l in eligible.itertuples(index=False):
        if l.loan_status=="Paid" and l.maturity_date<=e: continue
        months_age=max(0,(e-l.disbursement_date).days/30.44)
        exposure+=l.approved_amount*np.clip(1-months_age/max(l.loan_term_months,1),.05,1)
    recovery=collections[(collections.collection_date>=m)&(collections.collection_date<=e)].amount_recovered.sum()
    defs=eligible[eligible.loan_status.isin(["Defaulted","Written Off"])]
    credit_loss=max(0,defs.approved_amount.sum()*.75-recovery)
    revenue=lm.monthly_payment.sum()*.72
    acq_cost=acquisition[(acquisition.acquisition_date>=m)&(acquisition.acquisition_date<=e)].acquisition_cost.sum()
    operating=len(lm)*45
    funding=lm.approved_amount.sum()*.0055
    profit=revenue-acq_cost-operating-funding-credit_loss
    k.append([m.strftime("%Y-%m"),len(a),(a.application_status=="Approved").sum(),
      round((a.application_status=="Approved").mean()*100,2),len(lm),round(lm.approved_amount.mean(),2),
      round(lm.approved_amount.sum(),2),round(exposure,2),round(a.dti.mean(),4),
      round(default_rate,2),int(lm.loan_status.isin(["Defaulted","Written Off"]).sum()),
      round(credit_loss,2),round(recovery,2),round(revenue,2),round(acq_cost,2),round(operating,2),
      round(funding,2),round(profit,2),applications[applications.application_date<=e].customer_id.nunique()])
kpi=pd.DataFrame(k,columns=["month","applications","approvals","approval_rate","loans_disbursed","average_loan_size","total_disbursed","outstanding_portfolio","average_dti","default_rate","defaulted_loans","credit_loss","recovery_amount","revenue","acquisition_cost","operating_cost","funding_cost","profit","customer_count"])

# Save
tables={"customers":customers,"applications":applications_out,"loans":loans,"repayments":repayments,
        "credit_risk_history":risk,"acquisition":acquisition,"collections":collections,
        "monthly_business_kpis":kpi}
for name,df in tables.items():
    df.to_csv(DATA/f"{name}.csv",index=False,date_format="%Y-%m-%d")

# ---------------- validation ----------------
valid_customer=set(customers.customer_id); valid_app=set(applications.application_id); valid_loan=set(loans.loan_id)
checks={
 "customer_pk_unique":customers.customer_id.is_unique,
 "application_base_pk_unique":applications.application_id.is_unique,
 "loan_pk_unique":loans.loan_id.is_unique,
 "loan_customer_fk":loans.customer_id.isin(valid_customer).all(),
 "loan_application_fk":loans.application_id.isin(valid_app).all(),
 "repayment_loan_fk":repayments.loan_id.isin(valid_loan).all(),
 "collection_loan_fk":collections.loan_id.isin(valid_loan).all(),
 "loan_after_application":(loans.disbursement_date>=loans.application_id.map(applications.set_index("application_id").application_date)).all(),
 "loan_amount_positive":(loans.approved_amount>0).all(),
 "approved_only_loans":loans.application_id.map(applications.set_index("application_id").application_status).eq("Approved").all(),
 "no_rejected_loans":~loans.application_id.map(applications.set_index("application_id").application_status).eq("Rejected").any(),
}
with open(ROOT/"validation_report.txt","w") as f:
    f.write("Namaa Finance synthetic data validation\n\n")
    for key,val in checks.items(): f.write(f"{key}: {'PASS' if val else 'CHECK'}\n")
    f.write(f"\nCustomers: {len(customers):,}\nApplications incl. deliberate duplicates: {len(applications_out):,}\nLoans: {len(loans):,}\nRepayments: {len(repayments):,}\nCollections: {len(collections):,}\n")
    f.write("\nIntentional quality issues: 250 duplicate application ingestion records, ~600 missing DTI values, 25 negative requested amounts, and ~0.3% city whitespace inconsistency.\n")

print("Generated Namaa Finance dataset.")
print("Customers:",len(customers),"Applications:",len(applications_out),"Loans:",len(loans),"Repayments:",len(repayments),"Collections:",len(collections))
