# ==========================================================
# RECOMMENDATION ENGINE MODULE
# Financial Document Intelligence System
# Enterprise-Level Trusted Recommendation Engine
# Author: Vijay Project Integration
# ==========================================================

from datetime import datetime
from typing import List, Dict, Any


class RecommendationEngine:
    """
    Enterprise-grade Financial Recommendation Engine

    This engine analyzes user's financial health and provides
    trusted recommendations from:

    - Government schemes
    - RBI approved banks
    - SEBI regulated investments
    - IRDAI approved insurance
    - Safe financial practices

    Designed for popup UI integration and dashboard recommendation layer.
    """

    def __init__(self):

        self.engine_name = "Trusted Financial Recommendation Engine"
        self.version = "1.0 Enterprise"
        self.authority_sources = [
            "Government of India",
            "Reserve Bank of India (RBI)",
            "Securities and Exchange Board of India (SEBI)",
            "Insurance Regulatory and Development Authority of India (IRDAI)",
            "National Pension System Trust",
            "India Post",
            "Authorized Banking Institutions"
        ]

        # Trusted recommendations database
        self.trusted_recommendations = self._load_trusted_recommendations()

    # ==========================================================
    # LOAD TRUSTED RECOMMENDATIONS
    # ==========================================================

    def _load_trusted_recommendations(self) -> List[Dict[str, Any]]:
        """
        Load trusted financial recommendations from official sources
        """

        recommendations = [

            {
                "id": "GOV_PPF_001",
                "name": "Public Provident Fund (PPF)",
                "category": "Government Scheme",
                "authority": "Government of India",
                "risk_level": "Very Low",
                "description": (
                    "PPF is a long-term government-backed savings scheme "
                    "offering guaranteed returns and tax benefits under Section 80C."
                ),
                "benefits": [
                    "Government backed security",
                    "Tax free returns",
                    "Long term wealth creation",
                    "Low risk investment"
                ],
                "official_link": "https://www.indiapost.gov.in",
                "recommended_for": [
                    "Positive savings",
                    "Long term investment",
                    "Safe investors"
                ]
            },

            {
                "id": "GOV_NPS_002",
                "name": "National Pension System (NPS)",
                "category": "Pension Scheme",
                "authority": "Government of India",
                "risk_level": "Low",
                "description": (
                    "NPS is a government-sponsored pension scheme designed "
                    "to provide retirement income to citizens."
                ),
                "benefits": [
                    "Retirement planning",
                    "Tax benefits",
                    "Regulated by government",
                    "Long term financial security"
                ],
                "official_link": "https://www.npscra.nsdl.co.in",
                "recommended_for": [
                    "Working professionals",
                    "Retirement planning"
                ]
            },

            {
                "id": "GOV_APY_003",
                "name": "Atal Pension Yojana",
                "category": "Government Pension Scheme",
                "authority": "Government of India",
                "risk_level": "Very Low",
                "description": (
                    "APY is a government-backed pension scheme "
                    "providing guaranteed pension after retirement."
                ),
                "benefits": [
                    "Guaranteed pension",
                    "Government supported",
                    "Low investment requirement"
                ],
                "official_link": "https://financialservices.gov.in",
                "recommended_for": [
                    "Long term financial stability"
                ]
            },

            {
                "id": "BANK_SBI_FD_004",
                "name": "SBI Fixed Deposit",
                "category": "Bank Investment",
                "authority": "Reserve Bank of India Regulated Bank",
                "risk_level": "Very Low",
                "description": (
                    "Fixed Deposit offered by State Bank of India "
                    "with guaranteed returns and capital protection."
                ),
                "benefits": [
                    "Guaranteed returns",
                    "Safe bank investment",
                    "Capital protection"
                ],
                "official_link": "https://sbi.co.in",
                "recommended_for": [
                    "Safe savings",
                    "Short term investment"
                ]
            },

            {
                "id": "BANK_HDFC_RD_005",
                "name": "HDFC Recurring Deposit",
                "category": "Bank Savings",
                "authority": "RBI Regulated Bank",
                "risk_level": "Very Low",
                "description": (
                    "Recurring deposit allows systematic savings "
                    "with fixed interest and guaranteed returns."
                ),
                "benefits": [
                    "Disciplined savings",
                    "Guaranteed returns"
                ],
                "official_link": "https://www.hdfcbank.com",
                "recommended_for": [
                    "Regular savers"
                ]
            },

            {
                "id": "SEBI_SIP_006",
                "name": "Mutual Fund SIP (SEBI Regulated)",
                "category": "Investment",
                "authority": "SEBI",
                "risk_level": "Moderate",
                "description": (
                    "Systematic Investment Plan allows investing "
                    "in mutual funds regulated by SEBI."
                ),
                "benefits": [
                    "Wealth creation",
                    "Long term growth",
                    "SEBI regulated"
                ],
                "official_link": "https://www.amfiindia.com",
                "recommended_for": [
                    "Wealth building"
                ]
            },

            {
                "id": "INS_HEALTH_007",
                "name": "Health Insurance (IRDAI Approved)",
                "category": "Insurance",
                "authority": "IRDAI",
                "risk_level": "Protection",
                "description": (
                    "Health insurance protects against medical expenses "
                    "and financial emergencies."
                ),
                "benefits": [
                    "Medical financial protection",
                    "Emergency coverage"
                ],
                "official_link": "https://www.irdai.gov.in",
                "recommended_for": [
                    "Financial protection"
                ]
            }

        ]

        return recommendations

    # ==========================================================
    # DETECT POSITIVE SAVINGS
    # ==========================================================

    def detect_positive_savings(self, savings: float) -> bool:

        if savings is None:
            return False

        return savings > 0

    # ==========================================================
    # ANALYZE SAVINGS AND RETURN RECOMMENDATIONS
    # ==========================================================

    def analyze_savings(
        self,
        total_income: float,
        total_expense: float,
        savings: float
    ) -> Dict[str, Any]:

        result = {
            "engine": self.engine_name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "positive_savings": False,
            "recommendations": [],
            "message": ""
        }

        if self.detect_positive_savings(savings):

            result["positive_savings"] = True

            result["message"] = (
                "Congratulations! You have positive savings. "
                "Based on your financial profile, trusted "
                "recommendations are available."
            )

            result["recommendations"] = self.trusted_recommendations

        else:

            result["positive_savings"] = False

            result["message"] = (
                "Your savings are currently low. Focus on reducing expenses "
                "and increasing income."
            )

        return result

    # ==========================================================
    # GET RECOMMENDATIONS FOR UI DISPLAY
    # ==========================================================

    def get_recommendations_for_ui(self, savings: float):

        if savings > 0:
            return self.trusted_recommendations

        return []


# ==========================================================
# TEST FUNCTION (Optional)
# ==========================================================

if __name__ == "__main__":

    engine = RecommendationEngine()

    test_result = engine.analyze_savings(
        total_income=500000,
        total_expense=300000,
        savings=200000
    )

    print("Recommendation Engine Output:")
    print(test_result)
