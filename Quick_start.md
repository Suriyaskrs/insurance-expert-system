# 🚀 Quick Start Guide
## Insurance Claim Evaluation Expert System

---

## ⚡ 5-Minute Setup

### Step 1: Prerequisites
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install streamlit pandas
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run insurance_expert_system.py
```

### Step 4: Access the Interface
Your browser will automatically open to:
```
http://localhost:8501
```

---

## 🎯 Quick Usage Examples

### Example 1: Manual Entry - Approved Claim

1. Select **"Manual Entry"** mode
2. Enter these details:
   - Policy Type: `comprehensive`
   - Policy Start: `2024-01-01`
   - Policy End: `2025-01-01`
   - Loss Date: `2024-06-15`
   - Loss Type: `accident`
   - Claim Amount: `150000`
   - Sum Insured: `500000`
   - Deductible: `5000`
   - FIR Submitted: ✅ Yes
   - Documents Complete: ✅ Yes
   - Previous Claims: `1`

3. Click **"Evaluate Claim"**

**Expected Result:**
- ✅ Decision: APPROVED
- 💰 Payable Amount: ₹145,000
- 🟢 Fraud Risk: LOW

---

### Example 2: CSV Batch Processing

1. Select **"CSV Upload"** mode
2. Download the template CSV
3. Fill in your claims data
4. Upload the file
5. Click **"Evaluate All Claims"**
6. Download the results

**Sample CSV format:**
```csv
policy_type,policy_start_date,policy_end_date,loss_date,loss_type,claim_amount,sum_insured,deductible,fir_submitted,documents_complete,previous_claims
comprehensive,2024-01-01,2025-01-01,2024-06-15,accident,150000,500000,5000,yes,yes,1
third_party,2024-02-15,2025-02-15,2024-07-20,third_party_damage,80000,300000,3000,no,yes,0
```

---

## 📊 Understanding Results

### Decision Types

| Decision | Meaning | Icon |
|----------|---------|------|
| **APPROVED** | Claim meets all criteria | ✅ |
| **REJECTED** | Claim fails one or more rules | ❌ |
| **UNDER INVESTIGATION** | High fraud risk detected | 🔍 |

### Output Fields

- **Claim Validity**: Whether loss occurred in policy period
- **Coverage Status**: Whether loss type is covered
- **Payable Amount**: Final payout after deductible
- **Fraud Risk**: Low / Medium / High
- **Explanation**: Why this decision was made

---

## 🎓 Common Scenarios

### ✅ What Gets APPROVED?

A claim is approved when:
- ✅ Loss date is within policy period
- ✅ Loss type is covered under policy
- ✅ All mandatory documents are complete
- ✅ FIR is submitted (if required for theft/fire)
- ✅ Previous claims ≤ 2 (not high fraud risk)

**Example:**
```
Comprehensive policy
+ Accident on June 15, 2024
+ Policy valid Jan 1 - Dec 31, 2024
+ All documents submitted
+ 1 previous claim
= APPROVED ✅
```

---

### ❌ What Gets REJECTED?

Common rejection reasons:

**1. Coverage Issue**
```
Third-party policy
+ Own vehicle damage
= REJECTED (not covered)
```

**2. Policy Period Issue**
```
Loss date: Aug 10, 2024
Policy ended: July 31, 2024
= REJECTED (expired policy)
```

**3. Missing Documents**
```
Documents incomplete
= REJECTED (mandatory docs missing)
```

**4. Missing FIR**
```
Loss type: Theft
FIR submitted: No
= REJECTED (FIR mandatory)
```

---

### 🔍 What Goes UNDER INVESTIGATION?

Claims with high fraud risk:
```
Previous claims: 3 or more
= UNDER INVESTIGATION (high fraud risk)
```

These claims need manual review before approval/rejection.

---

## 💡 Tips & Tricks

### 1. Date Formats
The system accepts multiple date formats:
- `2024-01-15` (YYYY-MM-DD)
- `15/01/2024` (DD/MM/YYYY)
- `15-01-2024` (DD-MM-YYYY)

### 2. Boolean Values
For FIR and Documents in CSV:
- `yes`, `true`, `1`, `y` → True
- `no`, `false`, `0`, `n` → False

### 3. View Inference Trace
Click "View Inference Trace" to see exactly which rules fired and why!

### 4. Understanding Calculations
```
Admissible Loss = MIN(Claim Amount, Sum Insured)
Payable Amount = Admissible Loss - Deductible
```

**Example:**
```
Claim: ₹350,000
Sum Insured: ₹300,000
Deductible: ₹10,000

Admissible = MIN(350000, 300000) = 300,000
Payable = 300,000 - 10,000 = ₹290,000
```

---

## 🐛 Troubleshooting

### Issue: "Command not found: streamlit"
**Solution:**
```bash
pip install --upgrade streamlit
```

### Issue: "Invalid date format"
**Solution:** Use one of these formats:
- `YYYY-MM-DD`
- `DD/MM/YYYY`
- `DD-MM-YYYY`

### Issue: CSV upload fails
**Solution:**
- Check all required columns are present
- Ensure no empty cells
- Use the template as reference

### Issue: Port already in use
**Solution:**
```bash
streamlit run insurance_expert_system.py --server.port 8502
```

---

## 📞 Need Help?

### Check These First:
1. ✅ Python version ≥ 3.8
2. ✅ All dependencies installed
3. ✅ No syntax errors in CSV
4. ✅ Dates are in correct format

### Still Stuck?
- Review the full README.md
- Check the PROJECT_DOCUMENTATION.md
- Test with sample_claims_data.csv

---

## 🎯 Next Steps

### For Learning:
1. Try different claim scenarios
2. Experiment with edge cases
3. View the inference trace
4. Understand the rule logic

### For Development:
1. Read the source code comments
2. Review the knowledge base design
3. Test with your own data
4. Consider enhancements

### For Production Use:
1. Test thoroughly with real data
2. Document any custom rules needed
3. Set up monitoring
4. Train users on the interface

---

## 📚 Additional Resources

- **README.md** - Complete installation and usage guide
- **PROJECT_DOCUMENTATION.md** - Full technical documentation
- **sample_claims_data.csv** - Test data with 10 diverse claims
- **insurance_expert_system.py** - Source code with detailed comments

---

## ⭐ Quick Reference Card

### Input Requirements
- ✅ 11 required fields
- ✅ Valid dates
- ✅ Numeric amounts
- ✅ Boolean for yes/no

### Decision Rules
- ✅ Policy period check
- ✅ Coverage verification
- ✅ Document validation
- ✅ Fraud assessment

### Output Includes
- ✅ Decision (Approved/Rejected/Under Investigation)
- ✅ Payable amount
- ✅ Risk assessment
- ✅ Explanation
- ✅ Inference trace

---

**Ready to start? Run:**
```bash
streamlit run insurance_expert_system.py
```

**Have fun evaluating claims! 🎉**