"""
Seniority taxonomy for job-posting classification.

This file centralizes all seniority-level business rules.
No seniority keywords should be stored outside this file.
"""

SENIORITY_PRIORITY = [
    "Principal",
    "Manager",
    "Lead",
    "Senior",
    "Mid Level",
    "Junior",
    "Entry Level",
    "Unknown",
]

SENIORITY_KEYWORDS = {
    "Principal": [
        "principal",
        "distinguished",
        "chief",
        "architect",
        "10+ years",
        "10 years",
        "12+ years",
        "15+ years",
    ],

    "Manager": [
        "manager",
        "head of",
        "director",
        "supervisor",
        "manage a team",
        "team management",
        "direct reports",
        "people management",
        "hiring",
        "performance reviews",
    ],

    "Lead": [
        "lead",
        "team lead",
        "technical lead",
        "project lead",
        "lead analyst",
        "lead engineer",
        "lead data scientist",
        "8+ years",
        "8 years",
    ],

    "Senior": [
        "senior",
        "sr.",
        "sr ",
        "staff",
        "experienced",
        "mentor",
        "mentoring",
        "ownership",
        "strategic",
        "5+ years",
        "5 years",
        "6+ years",
        "7+ years",
    ],

    "Mid Level": [
        "mid-level",
        "mid level",
        "intermediate",
        "specialist",
        "consultant",
        "2+ years",
        "3+ years",
        "4+ years",
        "2 years",
        "3 years",
        "4 years",
    ],

    "Junior": [
        "junior",
        "jr.",
        "jr ",
        "associate",
        "assistant",
        "early career",
        "1+ years",
        "1 year",
        "0-2 years",
        "0 to 2 years",
    ],

    "Entry Level": [
        "entry level",
        "entry-level",
        "graduate",
        "trainee",
        "intern",
        "internship",
        "apprentice",
        "recent graduate",
        "no experience",
        "training provided",
        "willing to learn",
    ],
}