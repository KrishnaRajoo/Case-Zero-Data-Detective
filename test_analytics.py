from game.engine import InvestigationEngine


engine = InvestigationEngine()

df = engine.load_transactions(
    "data/transactions.csv"
)

df = engine.clean_transactions(df)

result = engine.detect_anomalies(df)

print("\n===== TRANSACTION ANALYSIS =====\n")

print(
    result[
        [
            "transaction_id",
            "suspect_id",
            "amount",
            "anomaly",
            "anomaly_score"
        ]
    ].to_string(index=False)
)


print("\n===== ANOMALOUS TRANSACTIONS =====\n")

print(
    result[
        result["anomaly"] == True
    ][
        [
            "transaction_id",
            "suspect_id",
            "amount"
        ]
    ].to_string(index=False)
)