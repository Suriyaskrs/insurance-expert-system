# 🛡️ Insurance Claim Evaluation Expert System

## Knowledge Engineering Project - Rule-Based Expert System

---

## 📖 Project Overview

This is an **Intelligent Insurance Claim Evaluation Expert System** built using **Knowledge Engineering principles**. The system uses a **rule-based approach** with **forward chaining inference** to automatically evaluate insurance claims.

### Key Features:
- ✅ Rule-based decision making (no machine learning)
- ✅ Forward chaining inference engine
- ✅ Natural language explanations
- ✅ Batch processing via CSV
- ✅ Interactive web interface
- ✅ Detailed inference trace for transparency

---

## 🎯 Domain

**Finance / Insurance** - General Insurance (Motor & Property Claims)

---

## 🏗️ System Architecture

```
INPUT FACTS → KNOWLEDGE BASE → INFERENCE ENGINE → DECISION + EXPLANATION
```

### Components:

1. **Knowledge Base**: Predefined insurance rules
2. **Inference Engine**: Forward chaining rule processor
3. **Working Memory**: Current claim facts
4. **Explanation Facility**: Natural language justification

---

## 📊 Input Fields

| Field               | Type    | Description                          |
|---------------------|---------|--------------------------------------|
| policy_type         | string  | comprehensive / third_party          |
| policy_start_date   | date    | Policy inception date                |
| policy_end_date     | date    | Policy expiry date                   |
| loss_date           | date    | Date of incident                     |
| loss_type           | string  | accident/theft/fire/own_damage/etc.  |
| claim_amount        | number  | Amount claimed                       |
| sum_insured         | number  | Maximum coverage                     |
| deductible          | number  | Policy excess                        |
| fir_submitted       | boolean | yes/no                               |
| documents_complete  | boolean | yes/no                               |
| previous_claims     | integer | Claims in last year                  |

---

## 📤 Output Fields

| Field            | Type    | Description                              |
|------------------|---------|------------------------------------------|
| claim_validity   | string  | valid / invalid                          |
| coverage_status  | string  | covered / not_covered                    |
| claim_decision   | string  | approved / rejected / under_investigation|
| payable_amount   | number  | Final payout after deductible            |
| fraud_risk       | string  | low / medium / high                      |
| explanation      | text    | Natural language justification           |

---

## 🧠 Rule Base

### 1. Policy Validity Rules
```
IF loss_date < policy_start_date OR loss_date > policy_end_date
THEN claim_validity = invalid
```

### 2. Coverage Rules
```
IF policy_type = "third_party" AND loss_type = "own_damage"
THEN coverage_status = not_covered

IF policy_type = "comprehensive" AND loss_type IN (accident, theft, fire)
THEN coverage_status = covered
```

### 3. Document Rules
```
IF loss_type IN (theft, fire) AND fir_submitted = no
THEN claim_decision = rejected

IF documents_complete = no
THEN claim_decision = rejected
```

### 4. Fraud Risk Rules
```
IF previous_claims >= 3 THEN fraud_risk = high
IF previous_claims = 2 THEN fraud_risk = medium
IF previous_claims <= 1 THEN fraud_risk = low
```

### 5. Investigation Rules
```
IF fraud_risk = high
THEN claim_decision = under_investigation
```

### 6. Approval Rules
```
IF claim_validity = valid
AND coverage_status = covered
AND documents_complete = yes
THEN claim_decision = approved
```

### 7. Payable Amount Calculation
```
admissible_loss = MIN(claim_amount, sum_insured)
payable_amount = MAX(0, admissible_loss - deductible)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone/Download the project

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the application
```bash
streamlit run insurance_expert_system.py
```

### Step 4: Access the web interface
The application will open automatically in your browser at:
```
http://localhost:8501
```

---

## 💻 Usage Guide

### Mode 1: Manual Entry

1. Select "Manual Entry" mode
2. Fill in the claim details:
   - Policy information (type, dates, coverage)
   - Claim information (loss date, type, amount)
   - Documentation status (FIR, documents)
   - Claim history
3. Click "Evaluate Claim"
4. View the decision, payable amount, and explanation
5. Expand "Inference Trace" to see the rule execution process

### Mode 2: CSV Batch Processing

1. Select "CSV Upload" mode
2. Download the sample CSV template
3. Fill in your claim data in the CSV file
4. Upload the completed CSV
5. Click "Evaluate All Claims"
6. View summary statistics and detailed results
7. Download the evaluated results with all decisions

---

## 📁 CSV File Format

**Required columns:**
```csv
policy_type,policy_start_date,policy_end_date,loss_date,loss_type,claim_amount,sum_insured,deductible,fir_submitted,documents_complete,previous_claims
comprehensive,2024-01-01,2025-01-01,2024-06-15,accident,150000,500000,5000,yes,yes,1
third_party,2024-02-15,2025-02-15,2024-07-20,third_party_damage,80000,300000,3000,no,yes,0
```

**Date Format:** YYYY-MM-DD or DD/MM/YYYY or DD-MM-YYYY  
**Boolean Format:** yes/no or true/false or 1/0

---

## 🔍 Example Scenarios

### Scenario 1: Approved Claim
```
Policy Type: comprehensive
Loss Type: accident
Loss Date: Within policy period
Documents: Complete
FIR: Not required for accident
Previous Claims: 1
→ DECISION: APPROVED
→ Payable: Claim amount - Deductible (capped at sum insured)
```

### Scenario 2: Rejected - Coverage Issue
```
Policy Type: third_party
Loss Type: own_damage
→ DECISION: REJECTED
→ Reason: Third-party policies don't cover own vehicle damage
```

### Scenario 3: Under Investigation
```
Previous Claims: 3 or more
→ DECISION: UNDER INVESTIGATION
→ Reason: High fraud risk detected
```

### Scenario 4: Rejected - Missing FIR
```
Loss Type: theft
FIR Submitted: No
→ DECISION: REJECTED
→ Reason: FIR mandatory for theft cases
```

---

## 🧪 Testing

### Test Case 1: Standard Approval
```python
Input:
- policy_type: comprehensive
- loss_date: 2024-06-15 (within policy period)
- loss_type: accident
- claim_amount: 150000
- sum_insured: 500000
- deductible: 5000
- fir_submitted: yes
- documents_complete: yes
- previous_claims: 1

Expected Output:
- claim_decision: approved
- payable_amount: 145000 (150000 - 5000)
- fraud_risk: low
```

### Test Case 2: Coverage Rejection
```python
Input:
- policy_type: third_party
- loss_type: own_damage

Expected Output:
- claim_decision: rejected
- coverage_status: not_covered
- payable_amount: 0
```

---

## 📚 Knowledge Engineering Principles Demonstrated

### 1. Knowledge Identification
- Domain: Insurance claim processing
- Expertise: Insurance policy rules, claim validation logic
- Sources: Insurance regulations, policy documents

### 2. Knowledge Representation
- Format: IF-THEN production rules
- Structure: Conditional logic with clear antecedents and consequents
- Organization: Modular rule sets for different aspects

### 3. Inference Mechanism
- Method: Forward chaining
- Process: Data-driven reasoning from facts to conclusions
- Execution: Sequential rule application with fact propagation

### 4. Explanation Facility
- Output: Natural language justification
- Trace: Complete inference path logging
- Transparency: Shows which rules fired and why

---

## 🎓 Academic Context

This project demonstrates core concepts from:
- **Artificial Intelligence**: Rule-based systems
- **Knowledge Engineering**: Expert system design
- **Logic Programming**: Declarative rule representation
- **Software Engineering**: Modular system architecture

---

## ⚙️ System Constraints

- ❌ No machine learning or neural networks
- ❌ No training or model fitting
- ✅ Pure rule-based logic
- ✅ Deterministic decisions
- ✅ Fully explainable reasoning
- ✅ Deductible always applied
- ✅ Payable amount never exceeds sum insured

---

## 📈 Future Enhancements

Potential extensions:
- Add more insurance product types
- Implement backward chaining for "what-if" analysis
- Add uncertainty handling (fuzzy logic)
- Create rule learning from historical data
- Add graphical rule visualization
- Implement multi-language support

---

## 🤝 Contributing

This is an academic project. For improvements:
1. Review the rule base
2. Test edge cases
3. Suggest additional rules
4. Improve explanation quality

---

## 📝 License

Academic/Educational Use

---

## 👥 Contact

For questions about this Knowledge Engineering project, please refer to the course instructor or teaching assistant.

---

## 🎯 Project Objectives Met

✅ **Knowledge Identification**: Defined insurance domain knowledge  
✅ **Knowledge Representation**: Implemented IF-THEN rules  
✅ **Inference Engine**: Built forward chaining system  
✅ **Explanation Facility**: Generated natural language justifications  
✅ **User Interface**: Created interactive web application  
✅ **Batch Processing**: Enabled CSV-based evaluation  
✅ **Documentation**: Comprehensive project documentation

---

**Built with:** Python, Streamlit, Pandas  
**Paradigm:** Rule-Based Expert System  
**Inference:** Forward Chaining  
**Domain:** Insurance / Finance
