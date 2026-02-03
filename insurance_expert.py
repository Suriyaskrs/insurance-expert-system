"""
Insurance Claim Evaluation Expert System
Knowledge Engineering Project
Rule-Based Expert System using Forward Chaining
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Tuple, List
import io


class InsuranceExpertSystem:
    """
    Expert System for Insurance Claim Evaluation
    Implements Knowledge Engineering principles with rule-based reasoning
    """
    
    def __init__(self):
        self.facts = {}
        self.inference_trace = []
        
    def reset(self):
        """Reset the system for a new evaluation"""
        self.facts = {}
        self.inference_trace = []
    
    def load_facts(self, input_data: Dict):
        """Load input facts into the knowledge base"""
        self.facts = input_data.copy()
        self.inference_trace.append("=== KNOWLEDGE BASE INITIALIZED ===")
        self.inference_trace.append(f"Input Facts: {list(input_data.keys())}")
    
    def evaluate_claim(self, input_data: Dict) -> Dict:
        """
        Main inference engine using forward chaining
        Applies rules sequentially to derive conclusions
        """
        self.reset()
        self.load_facts(input_data)
        
        # PHASE 1: Policy Validity Rules
        self._apply_policy_validity_rules()
        
        # PHASE 2: Coverage Rules
        self._apply_coverage_rules()
        
        # PHASE 3: Mandatory Document Rules
        self._apply_document_rules()
        
        # PHASE 4: Fraud Risk Assessment
        self._apply_fraud_risk_rules()
        
        # PHASE 5: Final Decision Rules
        self._apply_decision_rules()
        
        # PHASE 6: Payable Amount Calculation
        self._calculate_payable_amount()
        
        # PHASE 7: Generate Explanation
        explanation = self._generate_explanation()
        
        return {
            'claim_validity': self.facts.get('claim_validity', 'unknown'),
            'coverage_status': self.facts.get('coverage_status', 'unknown'),
            'claim_decision': self.facts.get('claim_decision', 'unknown'),
            'payable_amount': self.facts.get('payable_amount', 0),
            'fraud_risk': self.facts.get('fraud_risk', 'unknown'),
            'explanation': explanation,
            'inference_trace': self.inference_trace
        }
    
    def _apply_policy_validity_rules(self):
        """Rule 1: Check if loss occurred within policy period"""
        self.inference_trace.append("\n--- APPLYING POLICY VALIDITY RULES ---")
        
        loss_date = self.facts['loss_date']
        policy_start = self.facts['policy_start_date']
        policy_end = self.facts['policy_end_date']
        
        if loss_date < policy_start:
            self.facts['claim_validity'] = 'invalid'
            self.inference_trace.append(
                f"RULE FIRED: Loss date ({loss_date}) before policy start ({policy_start}) → claim_validity = INVALID"
            )
        elif loss_date > policy_end:
            self.facts['claim_validity'] = 'invalid'
            self.inference_trace.append(
                f"RULE FIRED: Loss date ({loss_date}) after policy end ({policy_end}) → claim_validity = INVALID"
            )
        else:
            self.facts['claim_validity'] = 'valid'
            self.inference_trace.append(
                f"RULE FIRED: Loss date within policy period → claim_validity = VALID"
            )
    
    def _apply_coverage_rules(self):
        """Rule 2 & 3: Check if loss type is covered under policy type"""
        self.inference_trace.append("\n--- APPLYING COVERAGE RULES ---")
        
        policy_type = self.facts['policy_type'].lower()
        loss_type = self.facts['loss_type'].lower()
        
        # Rule: Third party policies don't cover own damage
        if policy_type == 'third_party' and loss_type == 'own_damage':
            self.facts['coverage_status'] = 'not_covered'
            self.inference_trace.append(
                f"RULE FIRED: Third-party policy does not cover own damage → coverage_status = NOT COVERED"
            )
        
        # Rule: Comprehensive policies cover accident, theft, fire
        elif policy_type == 'comprehensive' and loss_type in ['accident', 'theft', 'fire', 'own_damage']:
            self.facts['coverage_status'] = 'covered'
            self.inference_trace.append(
                f"RULE FIRED: Comprehensive policy covers {loss_type} → coverage_status = COVERED"
            )
        
        # Rule: Third party damage covered by both policy types
        elif loss_type == 'third_party_damage':
            self.facts['coverage_status'] = 'covered'
            self.inference_trace.append(
                f"RULE FIRED: Third-party damage is covered → coverage_status = COVERED"
            )
        
        else:
            self.facts['coverage_status'] = 'not_covered'
            self.inference_trace.append(
                f"RULE FIRED: {loss_type} not covered under {policy_type} → coverage_status = NOT COVERED"
            )
    
    def _apply_document_rules(self):
        """Rule 4 & 5: Check mandatory documentation requirements"""
        self.inference_trace.append("\n--- APPLYING DOCUMENT RULES ---")
        
        loss_type = self.facts['loss_type'].lower()
        fir_submitted = self.facts['fir_submitted']
        documents_complete = self.facts['documents_complete']
        
        # Rule: FIR mandatory for theft and fire
        if loss_type in ['theft', 'fire'] and not fir_submitted:
            self.facts['claim_decision'] = 'rejected'
            self.facts['rejection_reason'] = 'FIR not submitted for theft/fire case'
            self.inference_trace.append(
                f"RULE FIRED: {loss_type.upper()} requires FIR, but not submitted → claim_decision = REJECTED"
            )
        
        # Rule: All documents must be complete
        elif not documents_complete:
            self.facts['claim_decision'] = 'rejected'
            self.facts['rejection_reason'] = 'Incomplete documentation'
            self.inference_trace.append(
                f"RULE FIRED: Documents incomplete → claim_decision = REJECTED"
            )
        
        else:
            self.inference_trace.append(
                f"RULE PASSED: All mandatory documents submitted"
            )
    
    def _apply_fraud_risk_rules(self):
        """Rule 7: Assess fraud risk based on previous claims"""
        self.inference_trace.append("\n--- APPLYING FRAUD RISK RULES ---")
        
        previous_claims = self.facts['previous_claims']
        
        if previous_claims >= 3:
            self.facts['fraud_risk'] = 'high'
            self.inference_trace.append(
                f"RULE FIRED: {previous_claims} previous claims (≥3) → fraud_risk = HIGH"
            )
        elif previous_claims == 2:
            self.facts['fraud_risk'] = 'medium'
            self.inference_trace.append(
                f"RULE FIRED: {previous_claims} previous claims (=2) → fraud_risk = MEDIUM"
            )
        else:
            self.facts['fraud_risk'] = 'low'
            self.inference_trace.append(
                f"RULE FIRED: {previous_claims} previous claim(s) (≤1) → fraud_risk = LOW"
            )
    
    def _apply_decision_rules(self):
        """Rule 6 & 8: Make final claim decision"""
        self.inference_trace.append("\n--- APPLYING FINAL DECISION RULES ---")
        
        # If already rejected, skip
        if self.facts.get('claim_decision') == 'rejected':
            self.inference_trace.append("RULE: Claim already rejected, no further evaluation needed")
            return
        
        claim_validity = self.facts.get('claim_validity')
        coverage_status = self.facts.get('coverage_status')
        fraud_risk = self.facts.get('fraud_risk')
        
        # Rule: High fraud risk requires investigation
        if fraud_risk == 'high':
            self.facts['claim_decision'] = 'under_investigation'
            self.inference_trace.append(
                f"RULE FIRED: High fraud risk → claim_decision = UNDER INVESTIGATION"
            )
        
        # Rule: Invalid claim or not covered = rejected
        elif claim_validity == 'invalid':
            self.facts['claim_decision'] = 'rejected'
            self.facts['rejection_reason'] = 'Claim outside policy period'
            self.inference_trace.append(
                f"RULE FIRED: Invalid claim → claim_decision = REJECTED"
            )
        
        elif coverage_status == 'not_covered':
            self.facts['claim_decision'] = 'rejected'
            self.facts['rejection_reason'] = 'Loss type not covered under policy'
            self.inference_trace.append(
                f"RULE FIRED: Not covered → claim_decision = REJECTED"
            )
        
        # Rule: All conditions met = approved
        elif claim_validity == 'valid' and coverage_status == 'covered':
            self.facts['claim_decision'] = 'approved'
            self.inference_trace.append(
                f"RULE FIRED: Valid claim + Covered loss + Documents OK → claim_decision = APPROVED"
            )
        
        else:
            self.facts['claim_decision'] = 'rejected'
            self.facts['rejection_reason'] = 'Does not meet approval criteria'
            self.inference_trace.append(
                f"RULE FIRED: Default rejection → claim_decision = REJECTED"
            )
    
    def _calculate_payable_amount(self):
        """Rule 6: Calculate payable amount if approved"""
        self.inference_trace.append("\n--- CALCULATING PAYABLE AMOUNT ---")
        
        decision = self.facts.get('claim_decision')
        
        if decision != 'approved':
            self.facts['payable_amount'] = 0
            self.inference_trace.append(f"Claim not approved → payable_amount = 0")
            return
        
        claim_amount = self.facts['claim_amount']
        sum_insured = self.facts['sum_insured']
        deductible = self.facts['deductible']
        
        # Admissible loss = minimum of claim amount and sum insured
        admissible_loss = min(claim_amount, sum_insured)
        self.inference_trace.append(
            f"Admissible Loss = MIN(claim_amount: {claim_amount}, sum_insured: {sum_insured}) = {admissible_loss}"
        )
        
        # Payable amount = admissible loss - deductible
        payable_amount = max(0, admissible_loss - deductible)
        self.facts['payable_amount'] = payable_amount
        self.inference_trace.append(
            f"Payable Amount = {admissible_loss} - {deductible} (deductible) = {payable_amount}"
        )
    
    def _generate_explanation(self) -> str:
        """Generate natural language explanation of the decision"""
        decision = self.facts.get('claim_decision')
        
        if decision == 'approved':
            explanation = (
                f"✅ CLAIM APPROVED: The claim is approved because the policy was active on the date of loss "
                f"({self.facts['loss_date']}), the incident type ({self.facts['loss_type']}) is covered under "
                f"the {self.facts['policy_type']} policy, and all mandatory documents were submitted. "
                f"The payable amount of ₹{self.facts['payable_amount']:,.2f} was calculated after applying "
                f"the deductible of ₹{self.facts['deductible']:,.2f}. "
            )
            if self.facts['fraud_risk'] == 'medium':
                explanation += "Note: Medium fraud risk detected due to previous claims history."
        
        elif decision == 'rejected':
            reason = self.facts.get('rejection_reason', 'Unknown reason')
            explanation = (
                f"❌ CLAIM REJECTED: The claim is rejected because {reason.lower()}. "
            )
            if self.facts.get('claim_validity') == 'invalid':
                explanation += (
                    f"The loss date ({self.facts['loss_date']}) falls outside the policy period "
                    f"({self.facts['policy_start_date']} to {self.facts['policy_end_date']}). "
                )
            elif self.facts.get('coverage_status') == 'not_covered':
                explanation += (
                    f"The policy type ({self.facts['policy_type']}) does not cover {self.facts['loss_type']}. "
                )
        
        elif decision == 'under_investigation':
            explanation = (
                f"🔍 UNDER INVESTIGATION: The claim is marked for investigation due to high fraud risk. "
                f"The claimant has {self.facts['previous_claims']} previous claims in the last year, "
                f"which exceeds the acceptable threshold. A detailed investigation will be conducted before "
                f"making a final decision. "
            )
        
        else:
            explanation = "Unable to determine claim status. Please review input data."
        
        return explanation


def parse_date(date_input) -> datetime:
    return pd.to_datetime(date_input, dayfirst=True).to_pydatetime()


def parse_boolean(bool_input) -> bool:
    """Parse boolean from various formats"""
    if isinstance(bool_input, bool):
        return bool_input
    if isinstance(bool_input, str):
        return bool_input.lower() in ['yes', 'true', '1', 'y']
    return bool(bool_input)


def process_csv(uploaded_file) -> pd.DataFrame:
    """Process uploaded CSV file and evaluate all claims"""
    # Read CSV
    df = pd.read_csv(uploaded_file)
    
    # Initialize expert system
    expert_system = InsuranceExpertSystem()
    
    # Prepare output columns
    results = []
    
    for idx, row in df.iterrows():
        # Prepare input data
        input_data = {
            'policy_type': str(row['policy_type']),
            'policy_start_date': parse_date(row['policy_start_date']),
            'policy_end_date': parse_date(row['policy_end_date']),
            'loss_date': parse_date(row['loss_date']),
            'loss_type': str(row['loss_type']),
            'claim_amount': float(row['claim_amount']),
            'sum_insured': float(row['sum_insured']),
            'deductible': float(row['deductible']),
            'fir_submitted': parse_boolean(row['fir_submitted']),
            'documents_complete': parse_boolean(row['documents_complete']),
            'previous_claims': int(row['previous_claims'])
        }
        
        # Evaluate claim
        result = expert_system.evaluate_claim(input_data)
        results.append(result)
    
    # Add results to dataframe
    df['claim_validity'] = [r['claim_validity'] for r in results]
    df['coverage_status'] = [r['coverage_status'] for r in results]
    df['claim_decision'] = [r['claim_decision'] for r in results]
    df['payable_amount'] = [r['payable_amount'] for r in results]
    df['fraud_risk'] = [r['fraud_risk'] for r in results]
    df['explanation'] = [r['explanation'] for r in results]
    
    return df


def main():
    """Streamlit UI for Insurance Expert System"""
    
    st.set_page_config(page_title="Insurance Claim Evaluator", layout="wide", page_icon="🛡️")
    
    st.title("🛡️ Insurance Claim Evaluation Expert System")
    st.markdown("**Knowledge Engineering Project | Rule-Based Expert System**")
    
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("ℹ️ About")
    st.sidebar.info(
        "This expert system evaluates insurance claims using:\n"
        "- **Knowledge Representation**: Rule-based logic\n"
        "- **Inference Engine**: Forward chaining\n"
        "- **Explanation Facility**: Natural language justification\n\n"
        "**Domain**: General Insurance (Motor/Property)"
    )
    
    # Mode selection
    mode = st.radio("**Select Input Mode:**", ["Manual Entry", "CSV Upload"], horizontal=True)
    
    if mode == "Manual Entry":
        st.header("📝 Manual Claim Entry")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Policy Details")
            policy_type = st.selectbox("Policy Type", ["comprehensive", "third_party"])
            policy_start_date = st.date_input("Policy Start Date")
            policy_end_date = st.date_input("Policy End Date")
            sum_insured = st.number_input("Sum Insured (₹)", min_value=0, value=500000, step=10000)
            deductible = st.number_input("Deductible/Excess (₹)", min_value=0, value=5000, step=1000)
        
        with col2:
            st.subheader("Claim Details")
            loss_date = st.date_input("Loss Date")
            loss_type = st.selectbox("Loss Type", 
                ["accident", "theft", "fire", "own_damage", "third_party_damage"])
            claim_amount = st.number_input("Claim Amount (₹)", min_value=0, value=100000, step=10000)
            fir_submitted = st.checkbox("FIR Submitted", value=False)
            documents_complete = st.checkbox("All Documents Complete", value=True)
            previous_claims = st.number_input("Previous Claims (Last Year)", min_value=0, value=0, step=1)
        
        if st.button("🔍 Evaluate Claim", type="primary", use_container_width=True):
            # Prepare input
            input_data = {
                'policy_type': policy_type,
                'policy_start_date': datetime.combine(policy_start_date, datetime.min.time()),
                'policy_end_date': datetime.combine(policy_end_date, datetime.min.time()),
                'loss_date': datetime.combine(loss_date, datetime.min.time()),
                'loss_type': loss_type,
                'claim_amount': float(claim_amount),
                'sum_insured': float(sum_insured),
                'deductible': float(deductible),
                'fir_submitted': fir_submitted,
                'documents_complete': documents_complete,
                'previous_claims': int(previous_claims)
            }
            
            # Run expert system
            expert_system = InsuranceExpertSystem()
            result = expert_system.evaluate_claim(input_data)
            
            st.markdown("---")
            st.header("📊 Evaluation Results")
            
            # Display decision with color coding
            decision = result['claim_decision']
            if decision == 'approved':
                st.success(f"**Decision:** {decision.upper()}")
            elif decision == 'rejected':
                st.error(f"**Decision:** {decision.upper()}")
            else:
                st.warning(f"**Decision:** {decision.upper()}")
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Claim Validity", result['claim_validity'].upper())
            with col2:
                st.metric("Coverage Status", result['coverage_status'].replace('_', ' ').upper())
            with col3:
                st.metric("Payable Amount", f"₹{result['payable_amount']:,.2f}")
            with col4:
                fraud_color = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
                st.metric("Fraud Risk", f"{fraud_color[result['fraud_risk']]} {result['fraud_risk'].upper()}")
            
            # Explanation
            st.subheader("💬 Explanation")
            st.info(result['explanation'])
            
            # Inference trace (expandable)
            with st.expander("🔬 View Inference Trace (Knowledge Engineering Process)"):
                for trace_line in result['inference_trace']:
                    st.text(trace_line)
    
    else:  # CSV Upload mode
        st.header("📂 Batch Evaluation via CSV")
        
        # Sample CSV download
        st.markdown("**Step 1:** Download the template CSV")
        sample_data = {
            'policy_type': ['comprehensive', 'third_party', 'comprehensive'],
            'policy_start_date': ['2024-01-01', '2024-02-15', '2023-12-01'],
            'policy_end_date': ['2025-01-01', '2025-02-15', '2024-12-01'],
            'loss_date': ['2024-06-15', '2024-07-20', '2024-08-10'],
            'loss_type': ['accident', 'third_party_damage', 'theft'],
            'claim_amount': [150000, 80000, 250000],
            'sum_insured': [500000, 300000, 600000],
            'deductible': [5000, 3000, 10000],
            'fir_submitted': ['yes', 'no', 'yes'],
            'documents_complete': ['yes', 'yes', 'yes'],
            'previous_claims': [1, 0, 3]
        }
        sample_df = pd.DataFrame(sample_data)
        
        csv_buffer = io.StringIO()
        sample_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="⬇️ Download Sample CSV Template",
            data=csv_buffer.getvalue(),
            file_name="insurance_claims_template.csv",
            mime="text/csv"
        )
        
        st.markdown("**Step 2:** Upload your filled CSV file")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            if st.button("🔍 Evaluate All Claims", type="primary", use_container_width=True):
                with st.spinner("Processing claims..."):
                    result_df = process_csv(uploaded_file)
                
                st.success(f"✅ Processed {len(result_df)} claims successfully!")
                
                st.subheader("📊 Results Summary")
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    approved = (result_df['claim_decision'] == 'approved').sum()
                    st.metric("Approved", approved, delta=f"{approved/len(result_df)*100:.1f}%")
                with col2:
                    rejected = (result_df['claim_decision'] == 'rejected').sum()
                    st.metric("Rejected", rejected, delta=f"{rejected/len(result_df)*100:.1f}%")
                with col3:
                    investigating = (result_df['claim_decision'] == 'under_investigation').sum()
                    st.metric("Under Investigation", investigating)
                with col4:
                    total_payout = result_df['payable_amount'].sum()
                    st.metric("Total Payout", f"₹{total_payout:,.0f}")
                
                # Display results table
                st.subheader("📋 Detailed Results")
                
                # Color code decision column
                def highlight_decision(row):
                    if row['claim_decision'] == 'approved':
                        return ['background-color: #d4edda'] * len(row)
                    elif row['claim_decision'] == 'rejected':
                        return ['background-color: #f8d7da'] * len(row)
                    else:
                        return ['background-color: #fff3cd'] * len(row)
                
                styled_df = result_df.style.apply(highlight_decision, axis=1)
                st.dataframe(styled_df, use_container_width=True)
                
                # Download processed CSV
                csv_output = io.StringIO()
                result_df.to_csv(csv_output, index=False)
                st.download_button(
                    label="⬇️ Download Evaluated Results",
                    data=csv_output.getvalue(),
                    file_name="evaluated_claims.csv",
                    mime="text/csv"
                )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Knowledge Engineering Project | Rule-Based Expert System | Forward Chaining Inference"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()