from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
REPORTS = Path("reports")


def main():
    # 1) Read CSVs into DataFrames (tables in memory)
    sent = pd.read_csv(RAW / "sent.csv", parse_dates=["send_ts"])
    events = pd.read_csv(RAW / "events.csv", parse_dates=["event_ts"])
    conversions = pd.read_csv(RAW / "conversions.csv", parse_dates=["conversion_ts"])

    # 2) Create a "send_date" column so we can group by day (not exact timestamps)
    sent["send_date"] = sent["send_ts"].dt.date

    # 3) SENT count per campaign/day (unique users)
    sent_counts = (
        sent.groupby(["campaign_id", "send_date"])["user_id"]
        .nunique()
        .reset_index(name="sent")
    )

    # 4) Attach send_date to each event by joining events to sent on user_id + campaign_id
    events_joined = events.merge(
        sent[["user_id", "campaign_id", "send_date"]],
        on=["user_id", "campaign_id"],
        how="inner"
    )

    # 5) Count unique users who opened/clicked/unsubscribed per campaign/day
    event_counts = (
        events_joined.groupby(["campaign_id", "send_date", "event_type"])["user_id"]
        .nunique()
        .unstack(fill_value=0)        # turn event_type values into columns
        .reset_index()
    )

    # Make sure these columns exist even if they don't appear in the data
    for col in ["open", "click", "unsubscribe"]:
        if col not in event_counts.columns:
            event_counts[col] = 0

    # 6) Attribute conversions to the same day/campaign (simple MVP attribution)
    conversions["conversion_date"] = conversions["conversion_ts"].dt.date
    conv_joined = conversions.merge(
        sent[["user_id", "campaign_id", "send_date"]],
        on="user_id",
        how="inner"
    )

    # Keep conversions that happen on/after the send_date (MVP logic)
    conv_joined = conv_joined[conv_joined["conversion_date"] >= conv_joined["send_date"]]

    conv_counts = (
        conv_joined.groupby(["campaign_id", "send_date"])["user_id"]
        .nunique()
        .reset_index(name="conversions")
    )

    # 7) Combine everything into one metrics table
    metrics = sent_counts.merge(event_counts, on=["campaign_id", "send_date"], how="left").fillna(0)
    metrics = metrics.merge(conv_counts, on=["campaign_id", "send_date"], how="left").fillna({"conversions": 0})

    # 8) Compute rates
    metrics["open_rate"] = metrics["open"] / metrics["sent"]
    metrics["ctr"] = metrics["click"] / metrics["sent"]
    metrics["unsubscribe_rate"] = metrics["unsubscribe"] / metrics["sent"]
    metrics["conversion_rate"] = metrics["conversions"] / metrics["sent"]

    # 9) Export to Excel
    REPORTS.mkdir(exist_ok=True)
    out_path = REPORTS / "email_campaign_report.xlsx"
    metrics.sort_values(["send_date", "campaign_id"]).to_excel(out_path, index=False)

    # 10) Print preview
    print(metrics.sort_values(["send_date", "campaign_id"]))
    print(f"\n✅ Wrote report to: {out_path}")


if __name__ == "__main__":
    main()
