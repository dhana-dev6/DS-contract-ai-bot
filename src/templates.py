"""
Standard Clause Templates for Similarity Matching and Risk Analysis.
These represent 'fair' or 'market standard' versions of common clauses.
"""

STANDARD_CLAUSES = {
    "Indemnity": """
    Each party (the "Indemnifying Party") agrees to indemnify, defend, and hold harmless the other party (the "Indemnified Party") from and against any and all third-party claims, damages, liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or related to the Indemnifying Party's gross negligence, willful misconduct, or material breach of this Agreement.
    """,
    
    "Termination for Convenience": """
    Either party may terminate this Agreement for any reason upon providing at least thirty (30) days' prior written notice to the other party. Upon such termination, the Client shall pay for all Services performed up to the effective date of termination.
    """,
    
    "Non-Compete": """
    During the Term of this Agreement and for a period of twelve (12) months thereafter, the Employee shall not directly or indirectly engage in or being employed by any business that is a direct competitor of the Company within the specific geographic region where the Company operates.
    """,
    
    "Confidentiality": """
    The Receiving Party shall hold and maintain the Confidential Information in confidence and shall not disclose it to any third party without the Disclosing Party's prior written consent, except as required by law. This obligation shall continue for a period of three (3) years following the termination of this Agreement.
    """
}

FULL_NDA_TEMPLATE = """1. Definition of Confidential Information.
For purposes of this Agreement, "Confidential Information" shall include all information or material that has or could have commercial value or other utility in the business in which Disclosing Party is engaged. If Confidential Information is in written form, the Disclosing Party shall label or stamp the materials with the word "Confidential" or some similar warning. If Confidential Information is transmitted orally, the Disclosing Party shall promptly provide a writing indicating that such oral communication constituted Confidential Information.

2. Exclusions from Confidential Information.
Receiving Party's obligations under this Agreement do not extend to information that is: (a) publicly known at the time of disclosure or subsequently becomes publicly known through no fault of the Receiving Party; (b) discovered or created by the Receiving Party before disclosure by Disclosing Party; (c) learned by the Receiving Party through legitimate means other than from the Disclosing Party or Disclosing Party's representatives; or (d) is disclosed by Receiving Party with Disclosing Party's prior written approval.

3. Obligations of Receiving Party.
Receiving Party shall hold and maintain the Confidential Information in strictest confidence for the sole and exclusive benefit of the Disclosing Party. Receiving Party shall carefully restrict access to Confidential Information to employees, contractors, and third parties as is reasonably required and shall require those persons to sign non-disclosure restrictions at least as protective as those in this Agreement. Receiving Party shall not, without the prior written approval of Disclosing Party, use for Receiving Party's own benefit, publish, copy, or otherwise disclose to others, or permit the use by others for their benefit or to the detriment of Disclosing Party, any Confidential Information. Receiving Party shall return to Disclosing Party any and all records, notes, and other written, printed, or tangible materials in its possession pertaining to Confidential Information immediately if Disclosing Party requests it in writing.

4. Time Periods.
The nondisclosure provisions of this Agreement shall survive the termination of this Agreement and Receiving Party's duty to hold Confidential Information in confidence shall remain in effect until the Confidential Information no longer qualifies as a trade secret or until Disclosing Party sends Receiving Party written notice releasing Receiving Party from this Agreement, whichever occurs first.

5. Relationships.
Nothing contained in this Agreement shall be deemed to constitute either party a partner, joint venturer or employee of the other party for any purpose.

6. Severability.
If a court finds any provision of this Agreement invalid or unenforceable, the remainder of this Agreement shall be interpreted so as best to effect the intent of the parties.

7. Integration.
This Agreement expresses the complete understanding of the parties with respect to the subject matter and supersedes all prior proposals, agreements, representations, and understandings. This Agreement may not be amended except in a writing signed by both parties.

8. Waiver.
The failure to exercise any right provided in this Agreement shall not be a waiver of prior or subsequent rights.
"""

FULL_EMPLOYMENT_TEMPLATE = """1. Employment.
The Company agrees to employ the Employee, and the Employee agrees to be employed by the Company, upon the terms and conditions set forth in this Agreement.

2. Term.
The employment of the Employee under this Agreement shall commence on [Start Date] and continue until terminated in accordance with the provisions of this Agreement.

3. Compensation.
The Company shall pay the Employee an annual base salary of $[Amount], payable in accordance with the Company's standard payroll schedule.

4. Duties and Responsibilities.
The Employee shall serve as [Job Title]. The Employee shall perform such duties and responsibilities as are customarily performed by persons in such position and such other duties as may be assigned from time to time by the Company.

5. Benefits.
The Employee shall be entitled to participate in all benefit plans and programs generally available to other employees of the Company, subject to the terms and conditions of such plans and programs.

6. Termination.
(a) For Cause. The Company may terminate the Employee's employment at any time for "Cause" (as defined in the Company's employee handbook).
(b) Without Cause. The Company may terminate the Employee's employment at any time without Cause upon two weeks' written notice.
(c) Resignation. The Employee may terminate their employment at any time upon two weeks' written notice to the Company.

7. Confidentiality.
The Employee acknowledges that during the course of employment, they will have access to confidential information of the Company. The Employee agrees not to disclose such confidential information to any third party, either during or after the term of employment.

8. Governing Law.
This Agreement shall be governed by and construed in accordance with the laws of the State of [State].

9. Entire Agreement.
This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior agreements and understandings, whether written or oral.
"""

