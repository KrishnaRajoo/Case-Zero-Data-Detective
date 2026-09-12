CASES = [

    # =========================================================
    # CASE 1 — EASY
    # =========================================================

    {
        "id": "case_001",

        "title": "The Missing Research Data",

        "difficulty": "EASY",

        "description": (
            "A confidential research dataset has disappeared "
            "from the university's Data Analytics Lab. "
            "Several people accessed the lab during the same "
            "period, but only one person had the opportunity "
            "and motive to remove the data."
        ),

        "culprit_id": "S03",

        "suspects": [

            {
                "id": "S01",
                "name": "Arjun Mehta",
                "role": "Data Analyst",
                "description": (
                    "Worked on the research project and "
                    "had legitimate access to the dataset."
                )
            },

            {
                "id": "S02",
                "name": "Neha Sharma",
                "role": "Research Assistant",
                "description": (
                    "Frequently worked in the laboratory "
                    "and assisted with data collection."
                )
            },

            {
                "id": "S03",
                "name": "Rohan Verma",
                "role": "System Administrator",
                "description": (
                    "Maintained the lab computers and had "
                    "administrative access to the systems."
                )
            }
        ],

        "clues": [

            {
                "id": "C01",
                "title": "Suspicious Login",
                "description": (
                    "A system administrator account was used "
                    "to access the research server late at night."
                ),
                "points": 100
            },

            {
                "id": "C02",
                "title": "Deleted File",
                "description": (
                    "The research dataset was deleted shortly "
                    "after the suspicious login."
                ),
                "points": 100
            },

            {
                "id": "C03",
                "title": "Access Log",
                "description": (
                    "The access log shows that the administrator "
                    "account was used from the laboratory computer."
                ),
                "points": 100
            }
        ]
    },


    # =========================================================
    # CASE 2 — MEDIUM
    # =========================================================

    {
        "id": "case_002",

        "title": "The Midnight Transaction",

        "difficulty": "MEDIUM",

        "description": (
            "A suspicious financial transaction has appeared "
            "inside the university's research funding system. "
            "₹48,750 was transferred shortly before midnight "
            "from a restricted project account to an unknown "
            "external account."
        ),

        "culprit_id": "S05",

        "suspects": [

            {
                "id": "S01",
                "name": "Aarav Malhotra",
                "role": "Finance Assistant",
                "description": (
                    "Processes routine financial transactions "
                    "and maintains payment records."
                )
            },

            {
                "id": "S02",
                "name": "Priya Nair",
                "role": "Research Coordinator",
                "description": (
                    "Manages the research project and "
                    "coordinates funding requirements."
                )
            },

            {
                "id": "S03",
                "name": "Kabir Singh",
                "role": "Data Analyst",
                "description": (
                    "Analyzes project data and occasionally "
                    "works with financial reports."
                )
            },

            {
                "id": "S04",
                "name": "Ishita Rao",
                "role": "Project Manager",
                "description": (
                    "Approves project expenses and monitors "
                    "research budgets."
                )
            },

            {
                "id": "S05",
                "name": "Vikram Joshi",
                "role": "System Administrator",
                "description": (
                    "Maintains the financial system and has "
                    "elevated technical privileges."
                )
            }
        ],

        "clues": [

            {
                "id": "C01",
                "title": "The Midnight Transfer",
                "description": (
                    "At 23:47, ₹48,750 was transferred from "
                    "the restricted research account to an "
                    "external account."
                ),
                "points": 100
            },

            {
                "id": "C02",
                "title": "Unusual Transaction Pattern",
                "description": (
                    "The transaction amount is significantly "
                    "different from the project's normal "
                    "payment pattern."
                ),
                "points": 100
            },

            {
                "id": "C03",
                "title": "System Access",
                "description": (
                    "The financial system records show that "
                    "an administrator account accessed the "
                    "transaction module shortly before the "
                    "transfer."
                ),
                "points": 100
            },

            {
                "id": "C04",
                "title": "After-Hours Activity",
                "description": (
                    "Security logs indicate that someone "
                    "entered the server room shortly before "
                    "the transaction occurred."
                ),
                "points": 100
            },

            {
                "id": "C05",
                "title": "Disconnected Device",
                "description": (
                    "A workstation connected to the financial "
                    "system suddenly disconnected shortly "
                    "after the transaction was completed."
                ),
                "points": 100
            },

            {
                "id": "C06",
                "title": "The Access Window",
                "description": (
                    "The transaction could only have been "
                    "completed during a short period when "
                    "administrative privileges were active."
                ),
                "points": 100
            },

            {
                "id": "C07",
                "title": "Conflicting Statement",
                "description": (
                    "One suspect claims they left the building "
                    "before midnight, but the access records "
                    "show activity associated with their "
                    "department after that time."
                ),
                "points": 100
            },

            {
                "id": "C08",
                "title": "System Privileges",
                "description": (
                    "Only a small number of employees had the "
                    "technical permissions required to modify "
                    "the transaction record without triggering "
                    "the normal approval workflow."
                ),
                "points": 100
            }
        ]
    },


    # =========================================================
    # CASE 3 — HARD
    # =========================================================

    {
        "id": "case_003",

        "title": "The Vanishing Ledger",

        "difficulty": "HARD",

        "description": (
            "A restricted university research fund has been "
            "drained through a series of carefully disguised "
            "transactions. The payments appear legitimate at "
            "first glance, but an analysis of transaction "
            "patterns, access records, and movement data reveals "
            "that someone manipulated the financial trail. "
            "Several suspects had access to different parts of "
            "the system, and at least one piece of evidence "
            "appears to have been deliberately planted."
        ),

        # The real culprit is NOT the most obvious suspect.
        "culprit_id": "S04",

        "suspects": [

            {
                "id": "S01",
                "name": "Arjun Mehta",
                "role": "Finance Officer",
                "description": (
                    "Responsible for processing research "
                    "payments and maintaining financial records. "
                    "He has direct access to transaction data "
                    "but claims he follows the normal approval "
                    "process for every payment."
                )
            },

            {
                "id": "S02",
                "name": "Neha Kapoor",
                "role": "Research Coordinator",
                "description": (
                    "Coordinates research projects and prepares "
                    "funding requests. She can view project "
                    "budgets and supporting documents but does "
                    "not normally approve financial transfers."
                )
            },

            {
                "id": "S03",
                "name": "Vikram Sethi",
                "role": "IT Administrator",
                "description": (
                    "Maintains university systems and has "
                    "elevated technical privileges. His account "
                    "appears in several unusual access logs "
                    "during the investigation."
                )
            },

            {
                "id": "S04",
                "name": "Riya Sharma",
                "role": "Procurement Manager",
                "description": (
                    "Handles vendor payments and procurement "
                    "requests. She has knowledge of approved "
                    "vendors and payment schedules and recently "
                    "had access to several restricted purchase "
                    "orders."
                )
            },

            {
                "id": "S05",
                "name": "Karan Malhotra",
                "role": "Department Assistant",
                "description": (
                    "Provides administrative support to the "
                    "research department. His access is limited, "
                    "but his movement records place him near "
                    "several important locations during the "
                    "investigation period."
                )
            }
        ],

        "clues": [

            # -------------------------------------------------
            # FINANCIAL EVIDENCE
            # -------------------------------------------------

            {
                "id": "C01",
                "title": "The First Transfer",
                "description": (
                    "At 21:18, ₹76,400 was transferred from "
                    "the restricted research account to a vendor "
                    "account that had previously received only "
                    "small payments."
                ),
                "points": 100
            },

            {
                "id": "C02",
                "title": "Split Payments",
                "description": (
                    "The original amount was divided into several "
                    "smaller transactions. Each individual payment "
                    "fell below the threshold that normally triggers "
                    "additional financial review."
                ),
                "points": 100
            },

            {
                "id": "C03",
                "title": "Repeated Vendor",
                "description": (
                    "The same vendor appeared in multiple "
                    "transactions over a short period, even though "
                    "there was no corresponding increase in "
                    "documented procurement activity."
                ),
                "points": 100
            },

            {
                "id": "C04",
                "title": "Unusual Timing",
                "description": (
                    "The suspicious payments were consistently "
                    "created outside the department's normal "
                    "working hours."
                ),
                "points": 100
            },

            # -------------------------------------------------
            # SYSTEM EVIDENCE
            # -------------------------------------------------

            {
                "id": "C05",
                "title": "Administrator Login",
                "description": (
                    "An administrator-level account accessed the "
                    "financial system shortly before several of "
                    "the suspicious payments were created."
                ),
                "points": 100
            },

            {
                "id": "C06",
                "title": "Modified Approval Record",
                "description": (
                    "One transaction contains an approval record "
                    "that was modified after the payment had "
                    "already been processed."
                ),
                "points": 100
            },

            {
                "id": "C07",
                "title": "The False Trail",
                "description": (
                    "A login associated with the IT department "
                    "appears to connect the suspicious activity "
                    "directly to the system administrator. "
                    "However, the timestamp contains a small "
                    "inconsistency that suggests the record "
                    "may have been manipulated."
                ),
                "points": 100
            },

            # -------------------------------------------------
            # MOVEMENT EVIDENCE
            # -------------------------------------------------

            {
                "id": "C08",
                "title": "Restricted Corridor",
                "description": (
                    "Movement records show that one suspect "
                    "entered the restricted finance corridor "
                    "shortly before the first suspicious transfer."
                ),
                "points": 100
            },

            {
                "id": "C09",
                "title": "The Missing Minutes",
                "description": (
                    "There is a short unexplained gap in one "
                    "suspect's movement history during the exact "
                    "period when two suspicious transactions "
                    "were created."
                ),
                "points": 100
            },

            # -------------------------------------------------
            # FINAL CONNECTION
            # -------------------------------------------------

            {
                "id": "C10",
                "title": "The Procurement Connection",
                "description": (
                    "A comparison of vendor records, transaction "
                    "timings, and movement data shows that the "
                    "same person had knowledge of the vendor, "
                    "access to the relevant documents, and an "
                    "opportunity to alter the payment trail."
                ),
                "points": 100
            }
        ]
    },

    # =========================================================
    # CASE 4 — MASTER CASE
    # =========================================================

    {
        "id": "case_004",

        "title": "The Aegis Conspiracy",

        "difficulty": "MASTER",

        "description": (
            "The three earlier investigations were not isolated "
            "crimes. Missing research data, suspicious financial "
            "transactions, and a vanished ledger are connected "
            "to a coordinated operation involving research theft "
            "and financial fraud. A final archive breach reveals "
            "that someone has been manipulating records to hide "
            "the entire conspiracy."
        ),

        "culprit_id": "S03",

        "suspects": [
            {
                "id": "S01",
                "name": "Dr. Ananya Mehra",
                "role": "Research Director",
                "description": (
                    "Directed Project Aegis and had legitimate "
                    "access to the confidential research archive."
                )
            },
            {
                "id": "S02",
                "name": "Arvind Kapoor",
                "role": "Finance Controller",
                "description": (
                    "Managed project budgets and financial "
                    "approvals."
                )
            },
            {
                "id": "S03",
                "name": "Vikram Sethi",
                "role": "IT Administrator",
                "description": (
                    "Had privileged access to research servers "
                    "and financial systems."
                )
            },
            {
                "id": "S04",
                "name": "Riya Sharma",
                "role": "Procurement Manager",
                "description": (
                    "Managed vendor records and procurement "
                    "transactions."
                )
            },
            {
                "id": "S05",
                "name": "Karan Malhotra",
                "role": "Research Coordinator",
                "description": (
                    "Coordinated research schedules and staff "
                    "activities."
                )
            },
            {
                "id": "S06",
                "name": "Meera Iyer",
                "role": "Deputy Registrar",
                "description": (
                    "Oversaw administrative compliance and "
                    "emergency document requests."
                )
            }
        ],

        "clues": [
            {
                "id": "C01",
                "title": "Aegis Archive Access",
                "description": (
                    "A restricted Project Aegis archive was "
                    "accessed shortly before the final incident."
                ),
                "points": 150
            },
            {
                "id": "C02",
                "title": "Deleted Research Package",
                "description": (
                    "A confidential research package was deleted "
                    "after a privileged system login."
                ),
                "points": 150
            },
            {
                "id": "C03",
                "title": "The Copied File",
                "description": (
                    "A temporary copy of the research data was "
                    "created before the original disappeared."
                ),
                "points": 150
            },
            {
                "id": "C04",
                "title": "Credential Misuse",
                "description": (
                    "A research director's credentials were used "
                    "during a period when movement records place "
                    "her elsewhere."
                ),
                "points": 150
            },
            {
                "id": "C05",
                "title": "The Aegis Vendor",
                "description": (
                    "A vendor payment is associated with a service "
                    "not included in the original research plan."
                ),
                "points": 150
            },
            {
                "id": "C06",
                "title": "Split Payments",
                "description": (
                    "Several smaller payments form a suspicious "
                    "pattern matching a larger unexplained amount."
                ),
                "points": 150
            },
            {
                "id": "C07",
                "title": "Modified Approval",
                "description": (
                    "A payment approval record was changed after "
                    "the payment had already been processed."
                ),
                "points": 150
            },
            {
                "id": "C08",
                "title": "The Midnight Transfer",
                "description": (
                    "A transfer occurred during the same "
                    "operational window as the archive access."
                ),
                "points": 150
            },
            {
                "id": "C09",
                "title": "Server Room Entry",
                "description": (
                    "Movement records show a suspect entering "
                    "the restricted server room during the "
                    "relevant period."
                ),
                "points": 150
            },
            {
                "id": "C10",
                "title": "The Missing Minutes",
                "description": (
                    "A gap in movement records overlaps the "
                    "research and financial activity."
                ),
                "points": 150
            },
            {
                "id": "C11",
                "title": "The False Alibi",
                "description": (
                    "A suspect's statement conflicts with a "
                    "verified movement record."
                ),
                "points": 150
            },
            {
                "id": "C12",
                "title": "The Shared Access Window",
                "description": (
                    "Two systems were accessed during a short "
                    "overlapping interval."
                ),
                "points": 150
            },
            {
                "id": "C13",
                "title": "Case 1 File Signature",
                "description": (
                    "A reference in the Master Case matches "
                    "the missing research package from Case 1."
                ),
                "points": 200
            },
            {
                "id": "C14",
                "title": "Case 2 Amount Pattern",
                "description": (
                    "The Master Case contains a transaction "
                    "pattern similar to the earlier midnight "
                    "transfer."
                ),
                "points": 200
            },
            {
                "id": "C15",
                "title": "Case 3 Ledger Reference",
                "description": (
                    "A recovered record points to the same "
                    "vendor or account connected to the missing "
                    "ledger."
                ),
                "points": 200
            },
            {
                "id": "C16",
                "title": "The Final Link",
                "description": (
                    "The same person had the technical access, "
                    "operational knowledge, and opportunity "
                    "to coordinate the entire operation."
                ),
                "points": 250
            }
        ]
    }
]

