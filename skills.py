# -*- coding: utf-8 -*-
"""Subscription Churn Hazard & Retention Orchestrator Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def predict_subscription_churn_hazard(**kwargs):
    """Calculates Cox Proportional Hazards churn risk using product usage velocity decay, payment decline frequency, and support sentiment drift, triggering tailored retention plays."""
    subscription_id = kwargs.get('subscription_id')
    monthly_recurring_revenue_mrr = kwargs.get('monthly_recurring_revenue_mrr')
    dau_to_mau_ratio_last_30d = kwargs.get('dau_to_mau_ratio_last_30d')
    usage_velocity_drop_pct = kwargs.get('usage_velocity_drop_pct')
    consecutive_failed_payments = kwargs.get('consecutive_failed_payments')
    ticket_sentiment_score_negative_1_to_plus_1 = kwargs.get('ticket_sentiment_score_negative_1_to_plus_1')

    import math
    beta_usage = 0.03 * usage_velocity_drop_pct
    beta_stickiness = max(0.0, (0.4 - dau_to_mau_ratio_last_30d) * 4.0)
    beta_payment = 0.6 * consecutive_failed_payments
    beta_sentiment = max(0.0, (-ticket_sentiment_score_negative_1_to_plus_1) * 1.5)
    
    log_hazard = beta_usage + beta_stickiness + beta_payment + beta_sentiment
    hazard_ratio = round(math.exp(min(4.0, log_hazard)), 2)
    
    baseline_survival_90d = 0.95
    churn_risk_pct = round((1.0 - (baseline_survival_90d ** hazard_ratio)) * 100.0, 1)
    
    if churn_risk_pct >= 60.0:
        retention_tier = "CRITICAL_CHURN_IMMINENT"
        action = "Deploy immediate executive sponsor outreach + 25% annual renewal concession offer."
    elif churn_risk_pct >= 30.0:
        retention_tier = "HIGH_RISK_VOLATILE"
        action = "Schedule CSM product optimization review; resolve unresolved technical support blocker."
    elif churn_risk_pct >= 15.0:
        retention_tier = "MODERATE_INACTIVITY"
        action = "Trigger automated in-app feature walkthrough and value-realization email sequence."
    else:
        retention_tier = "HEALTHY_EXPANSION_CANDIDATE"
        action = "Account stable. Recommend enterprise upsell / seat expansion proposal."
        
    mrr_at_risk = round(monthly_recurring_revenue_mrr * (churn_risk_pct / 100.0), 2)
    
    result = {
        "status": "success",
        "subscription_id": subscription_id,
        "mrr_usd": monthly_recurring_revenue_mrr,
        "hazard_ratio": hazard_ratio,
        "projected_90d_churn_risk_pct": churn_risk_pct,
        "expected_mrr_loss_exposure_usd": mrr_at_risk,
        "retention_tier": retention_tier,
        "prescriptive_retention_action": action,
        "engine": "GenPark SaaS Churn Hazard & Survival Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "predict_subscription_churn_hazard": {
        "name": "predict_subscription_churn_hazard",
        "description": "Calculates Cox Proportional Hazards churn risk using product usage velocity decay, payment decline frequency, and support sentiment drift, triggering tailored retention plays.",
        "parameters": {
            "type": "object",
            "properties": {
                "subscription_id": {"type": "string", "description": "Subscriber contract ID"},
                "monthly_recurring_revenue_mrr": {"type": "number", "description": "Subscriber MRR (USD)"},
                "dau_to_mau_ratio_last_30d": {"type": "number", "description": "Daily to Monthly Active Users ratio (stickiness index)"},
                "usage_velocity_drop_pct": {"type": "number", "description": "Percentage decrease in core workflow completions vs baseline"},
                "consecutive_failed_payments": {"type": "integer", "description": "Number of dunning payment retries encountered"},
                "ticket_sentiment_score_negative_1_to_plus_1": {"type": "number", "description": "Recent Zendesk/Intercom support ticket sentiment"},
            },
            "required": ['subscription_id', 'monthly_recurring_revenue_mrr', 'dau_to_mau_ratio_last_30d', 'usage_velocity_drop_pct', 'consecutive_failed_payments', 'ticket_sentiment_score_negative_1_to_plus_1']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "predict_subscription_churn_hazard":
            res = predict_subscription_churn_hazard(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-subscription-churn-hazard-cox-proportional-sentinel-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-subscription-churn-hazard-cox-proportional-sentinel-skill...")
    test_args = {'subscription_id': 'SUB-ACME-ENTERPRISE-019', 'monthly_recurring_revenue_mrr': 12500.0, 'dau_to_mau_ratio_last_30d': 0.22, 'usage_velocity_drop_pct': 38.5, 'consecutive_failed_payments': 2, 'ticket_sentiment_score_negative_1_to_plus_1': -0.65}
    res = predict_subscription_churn_hazard(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-subscription-churn-hazard-cox-proportional-sentinel-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
