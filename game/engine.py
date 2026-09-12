import pandas as pd

from sklearn.ensemble import IsolationForest


class InvestigationEngine:

    def __init__(self):
        self.suspicion_scores = {}

    # =========================================================
    # TRANSACTIONS
    # =========================================================

    def load_transactions(self, filepath, case_id=None):

        df = pd.read_csv(filepath)

        if case_id and "case_id" in df.columns:

            df = df[
                df["case_id"].astype(str) == str(case_id)
            ].copy()

        return df

    def clean_transactions(self, df):

        df = df.copy()

        # Convert amount to numeric
        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        # Remove invalid amounts
        df = df.dropna(
            subset=["amount"]
        )

        # Convert date
        if "date" in df.columns:

            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            )

        return df

    # =========================================================
    # ANOMALY DETECTION
    # =========================================================

    def detect_anomalies(self, df):

        df = df.copy()

        # Always create these columns
        df["anomaly"] = False
        df["anomaly_score"] = 0.0

        if "transaction_type" not in df.columns:

            return df

        # Only analyze purchases
        purchase_mask = (
            df["transaction_type"]
            .astype(str)
            .str.lower()
            == "purchase"
        )

        purchase_data = df[
            purchase_mask
        ].copy()

        # Isolation Forest requires enough records
        if len(purchase_data) < 5:

            return purchase_data

        model = IsolationForest(
            contamination=0.15,
            random_state=42
        )

        model.fit(
            purchase_data[
                ["amount"]
            ]
        )

        purchase_data[
            "anomaly_prediction"
        ] = model.predict(
            purchase_data[
                ["amount"]
            ]
        )

        purchase_data[
            "anomaly_score"
        ] = -model.decision_function(
            purchase_data[
                ["amount"]
            ]
        )

        purchase_data[
            "anomaly"
        ] = (
            purchase_data[
                "anomaly_prediction"
            ] == -1
        )

        return purchase_data

    # =========================================================
    # BASIC SUSPICION SCORE
    # =========================================================

    def calculate_suspicion(
        self,
        suspects,
        transactions
    ):

        scores = {}

        # Normalize suspect IDs
        if "suspect_id" in transactions.columns:

            transactions = transactions.copy()

            transactions[
                "suspect_id"
            ] = transactions[
                "suspect_id"
            ].astype(str)

        for suspect in suspects:

            suspect_id = str(
                suspect["id"]
            )

            suspect_transactions = (
                transactions[
                    transactions[
                        "suspect_id"
                    ].astype(str)
                    == suspect_id
                ]
            )

            score = 0

            # ---------------------------------------------
            # ANOMALOUS TRANSACTIONS
            # ---------------------------------------------

            if "anomaly" in suspect_transactions.columns:

                anomalies = (
                    suspect_transactions[
                        suspect_transactions[
                            "anomaly"
                        ] == True
                    ]
                )

                score += (
                    len(anomalies) * 20
                )

            # ---------------------------------------------
            # HIGH VALUE TRANSACTIONS
            # ---------------------------------------------

            high_value = (
                suspect_transactions[
                    suspect_transactions[
                        "amount"
                    ] > 10000
                ]
            )

            score += (
                len(high_value) * 15
            )

            # ---------------------------------------------
            # ROLE RELEVANCE
            # ---------------------------------------------

            if suspect.get("role") == "IT Technician":

                score += 20

            # Keep score within 100
            score = min(
                score,
                100
            )

            scores[
                suspect_id
            ] = score

        self.suspicion_scores = scores

        return scores

    # =========================================================
    # INVESTIGATION INSIGHTS
    # =========================================================

    def generate_insight(
        self,
        transactions,
        suspicion_scores
    ):

        insights = []

        # ---------------------------------------------
        # Highest transaction
        # ---------------------------------------------

        if not transactions.empty:

            highest = transactions.loc[
                transactions[
                    "amount"
                ].idxmax()
            ]

            insights.append(
                f"The highest transaction was "
                f"₹{highest['amount']:,.0f} "
                f"and belongs to "
                f"{highest['suspect_id']}."
            )

        # ---------------------------------------------
        # Most anomalies
        # ---------------------------------------------

        if (
            "anomaly" in transactions.columns
            and "suspect_id" in transactions.columns
        ):

            anomaly_counts = (
                transactions[
                    transactions[
                        "anomaly"
                    ] == True
                ]
                .groupby(
                    "suspect_id"
                )
                .size()
            )

            if not anomaly_counts.empty:

                most_anomalous = (
                    anomaly_counts.idxmax()
                )

                count = (
                    anomaly_counts.max()
                )

                insights.append(
                    f"{most_anomalous} has the highest "
                    f"number of detected anomalous "
                    f"transactions ({count})."
                )

        # ---------------------------------------------
        # Highest suspicion
        # ---------------------------------------------

        if suspicion_scores:

            highest_risk = max(
                suspicion_scores,
                key=suspicion_scores.get
            )

            insights.append(
                f"The current highest-risk suspect is "
                f"{highest_risk}."
            )

        return insights

    # =========================================================
    # MOVEMENTS
    # =========================================================

    def load_movements(
        self,
        filepath,
        case_id=None
    ):

        df = pd.read_csv(filepath)

        if case_id and "case_id" in df.columns:

            df = df[
                df["case_id"].astype(str)
                == str(case_id)
            ].copy()

        return df

    def clean_movements(self, df):

        df = df.copy()

        # Convert date
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        # Make sure time exists
        if "time" not in df.columns:

            df["time"] = "00:00:00"

        df["time"] = (
            df["time"]
            .astype(str)
        )

        # Combine date + time
        df["timestamp"] = pd.to_datetime(
            df["date"].dt.strftime(
                "%Y-%m-%d"
            )
            + " "
            + df["time"],
            errors="coerce"
        )

        # Remove invalid timestamps
        df = df.dropna(
            subset=["timestamp"]
        )

        # Sort chronologically
        df = df.sort_values(
            "timestamp"
        ).reset_index(
            drop=True
        )

        return df

    # =========================================================
    # MOVEMENT FILTERS
    # =========================================================

    def filter_movements(
        self,
        df,
        suspect=None,
        location=None
    ):

        result = df.copy()

        if (
            suspect
            and suspect != "ALL"
        ):

            result = result[
                result[
                    "suspect_id"
                ].astype(str)
                == str(suspect)
            ]

        if (
            location
            and location != "ALL"
        ):

            result = result[
                result[
                    "location"
                ] == location
            ]

        return result

    # =========================================================
    # TIMELINE
    # =========================================================

    def build_timeline(
        self,
        movements
    ):

        timeline = []

        for _, row in movements.iterrows():

            timeline.append({

                "event_id":
                    row["event_id"],

                "suspect_id":
                    row["suspect_id"],

                "time":
                    row["time"],

                "location":
                    row["location"],

                "event_type":
                    row["event_type"],

                "description":
                    row["description"]

            })

        return timeline

    # =========================================================
    # CONNECTED EVENTS
    # =========================================================

    def find_connected_events(
        self,
        movements,
        max_minutes=10
    ):

        movements = (
            movements
            .sort_values(
                "timestamp"
            )
            .reset_index(
                drop=True
            )
        )

        connections = []

        for i in range(
            len(movements)
        ):

            current = movements.iloc[i]

            for j in range(
                i + 1,
                len(movements)
            ):

                next_event = (
                    movements.iloc[j]
                )

                difference = (
                    next_event["timestamp"]
                    - current["timestamp"]
                )

                minutes = (
                    difference.total_seconds()
                    / 60
                )

                if minutes > max_minutes:

                    break

                # Same suspect only
                if (
                    str(
                        current["suspect_id"]
                    )
                    !=
                    str(
                        next_event["suspect_id"]
                    )
                ):

                    continue

                connections.append({

                    "suspect_id":
                        current["suspect_id"],

                    "event_1":
                        current["event_id"],

                    "event_2":
                        next_event["event_id"],

                    "time_difference":
                        round(
                            minutes,
                            1
                        ),

                    "location_1":
                        current["location"],

                    "location_2":
                        next_event["location"]

                })

        return connections

    # =========================================================
    # INTELLIGENCE REPORT
    # =========================================================

    def build_intelligence_report(
        self,
        transactions,
        movements,
        suspects
    ):

        report = []

        # =====================================================
        # TRANSACTION STATISTICS
        # =====================================================

        if transactions.empty:

            transaction_stats = pd.DataFrame(
                columns=[
                    "suspect_id",
                    "transaction_count",
                    "total_spending",
                    "average_transaction",
                    "maximum_transaction",
                    "anomaly_count"
                ]
            )

        else:

            transaction_stats = (
                transactions
                .groupby(
                    "suspect_id"
                )
                .agg(

                    transaction_count=(
                        "amount",
                        "count"
                    ),

                    total_spending=(
                        "amount",
                        "sum"
                    ),

                    average_transaction=(
                        "amount",
                        "mean"
                    ),

                    maximum_transaction=(
                        "amount",
                        "max"
                    ),

                    anomaly_count=(
                        "anomaly",
                        "sum"
                    )

                )
                .reset_index()
            )

        # =====================================================
        # MOVEMENT STATISTICS
        # =====================================================

        if movements.empty:

            movement_stats = pd.DataFrame(
                columns=[
                    "suspect_id",
                    "event_count",
                    "unique_locations"
                ]
            )

        else:

            movement_stats = (
                movements
                .groupby(
                    "suspect_id"
                )
                .agg(

                    event_count=(
                        "event_id",
                        "count"
                    ),

                    unique_locations=(
                        "location",
                        "nunique"
                    )

                )
                .reset_index()
            )

        # =====================================================
        # MERGE
        # =====================================================

        stats = transaction_stats.merge(
            movement_stats,
            on="suspect_id",
            how="outer"
        )

        stats = stats.fillna(0)

        # =====================================================
        # MAKE EVERY SUSPECT APPEAR
        # =====================================================

        known_ids = set(
            stats[
                "suspect_id"
            ]
            .astype(str)
        )

        for suspect in suspects:

            suspect_id = str(
                suspect["id"]
            )

            if suspect_id not in known_ids:

                stats.loc[
                    len(stats)
                ] = {

                    "suspect_id":
                        suspect["id"],

                    "transaction_count":
                        0,

                    "total_spending":
                        0,

                    "average_transaction":
                        0,

                    "maximum_transaction":
                        0,

                    "anomaly_count":
                        0,

                    "event_count":
                        0,

                    "unique_locations":
                        0
                }

        # =====================================================
        # CALCULATE RISK
        # =====================================================

        for _, row in stats.iterrows():

            suspect_id = str(
                row["suspect_id"]
            )

            score = 0

            reasons = []

            # ---------------------------------------------
            # ANOMALIES
            # ---------------------------------------------

            anomaly_count = int(
                row[
                    "anomaly_count"
                ]
            )

            if anomaly_count > 0:

                anomaly_points = min(
                    anomaly_count * 15,
                    35
                )

                score += anomaly_points

                reasons.append(
                    f"{anomaly_count} anomalous "
                    f"transaction(s)"
                )

            # ---------------------------------------------
            # HIGH VALUE TRANSACTION
            # ---------------------------------------------

            maximum_transaction = float(
                row[
                    "maximum_transaction"
                ]
            )

            if maximum_transaction >= 50000:

                score += 20

                reasons.append(
                    "High-value transaction detected"
                )

            elif maximum_transaction >= 25000:

                score += 10

                reasons.append(
                    "Significant transaction detected"
                )

            # ---------------------------------------------
            # TOTAL SPENDING
            # ---------------------------------------------

            total_spending = float(
                row[
                    "total_spending"
                ]
            )

            if total_spending >= 100000:

                score += 15

                reasons.append(
                    "Unusually high total spending"
                )

            elif total_spending >= 50000:

                score += 8

                reasons.append(
                    "Elevated total spending"
                )

            # ---------------------------------------------
            # TRANSACTION FREQUENCY
            # ---------------------------------------------

            transaction_count = int(
                row[
                    "transaction_count"
                ]
            )

            if transaction_count >= 8:

                score += 5

                reasons.append(
                    "High transaction frequency"
                )

            # ---------------------------------------------
            # TIMELINE ACTIVITY
            # ---------------------------------------------

            event_count = int(
                row[
                    "event_count"
                ]
            )

            if event_count >= 6:

                score += 10

                reasons.append(
                    "High activity in event timeline"
                )

            elif event_count >= 4:

                score += 5

                reasons.append(
                    "Repeated timeline activity"
                )

            # ---------------------------------------------
            # LOCATION DIVERSITY
            # ---------------------------------------------

            unique_locations = int(
                row[
                    "unique_locations"
                ]
            )

            if unique_locations >= 4:

                score += 5

                reasons.append(
                    "Activity across multiple locations"
                )

            # ---------------------------------------------
            # FINAL SCORE
            # ---------------------------------------------

            score = min(
                score,
                100
            )

            report.append({

                "suspect_id":
                    suspect_id,

                "transaction_count":
                    transaction_count,

                "total_spending":
                    round(
                        total_spending,
                        2
                    ),

                "average_transaction":
                    round(
                        float(
                            row[
                                "average_transaction"
                            ]
                        ),
                        2
                    ),

                "maximum_transaction":
                    round(
                        maximum_transaction,
                        2
                    ),

                "anomaly_count":
                    anomaly_count,

                "event_count":
                    event_count,

                "unique_locations":
                    unique_locations,

                "risk_score":
                    score,

                "reasons":
                    reasons

            })

        # =====================================================
        # HIGHEST RISK FIRST
        # =====================================================

        report.sort(
            key=lambda x:
                x["risk_score"],
            reverse=True
        )

        return report

