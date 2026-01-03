Email Campaign for Health Care

## Overview
This project implements an end-to-end analytics pipeline for evaluating email campaign performance in a healthcare context. It connects messaging engagement (opens, clicks, unsubscribes) with downstream care-related actions to support data-driven growth and product decisions.
It's main purpose is to see how one would make meaningful deductions and improvements. 

___

## Problem Statement
For a healthcare team, no matter if it is insurance or benefits, usability of products and creating trust are paramount for success. Some questions one would have is- 
"How are these campaigns performing across channels and funnels?"
"Which campaigns are sticking with members and causing them to go deeper?"
"Which campaigns / what sort of content causes members to unsubrscibe and disengage?"
___

## Data Sources
The data for this has three sources. These were made up by me. 

- **sent.csv 
  Records when a user is sent a specific campaign.

- **events.csv
  Tracks engagement events such as opens, clicks, and unsubscribes.

- **conversions.csv 
  Represents downstream care-related actions (e.g., appointment booked)
___

## Metrics
Metrics are aggregated at the campaign + day level.

Sent (unique users) (sent.groupby(["campaign_id", "send_date"])["user_id"].nunique())
Opens, Clicks, Unsubscribes 
Conversions into care-related actions
Open Rate
Click-Through Rate (CTR)
Unsubscribe Rate
Conversion Rate

Rates are calculated using **sent** as the denominator to maintain consistent interpretation.

___

## Output
The pipeline generates:
An Excel report suitable for stakeholder consumption
A printed console preview for quick validation

Output files are written to the `reports/` directory (gitignored).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp data/sample/*.csv data/raw/
python run_report.py
