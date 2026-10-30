# Subscription Churn Hazard & Retention Orchestrator Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `predict_subscription_churn_hazard`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates Cox Proportional Hazards churn risk using product usage velocity decay, payment decline frequency, and support sentiment drift, triggering tailored retention plays.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (SaaS & Subscription Commerce)`

## MCP Tool Specification
### `predict_subscription_churn_hazard`
Parameters:
- `subscription_id` (str): Subscriber contract ID
- `monthly_recurring_revenue_mrr` (float): Subscriber MRR (USD)
- `dau_to_mau_ratio_last_30d` (float): Daily to Monthly Active Users ratio (stickiness index)
- `usage_velocity_drop_pct` (float): Percentage decrease in core workflow completions vs baseline
- `consecutive_failed_payments` (int): Number of dunning payment retries encountered
- `ticket_sentiment_score_negative_1_to_plus_1` (float): Recent Zendesk/Intercom support ticket sentiment

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-subscription-churn-hazard-cox-proportional-sentinel-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-subscription-churn-hazard-cox-proportional-sentinel-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
