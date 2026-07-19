# ADR-0002 — Risk Intelligence Engine (RIE) Design

Version: 1.0  
Status: Accepted  
Project: ARPI Enterprise

---

# 1. Decision Title

Adoption of an Independent Risk Intelligence Engine Architecture

---

# 2. Context

Risk analysis is a core capability of ARPI Enterprise.

The initial Market Engine provided market signals and basic risk indicators, but risk evaluation requires an independent intelligence layer capable of receiving signals from multiple future engines.

The system requires a dedicated Risk Intelligence Engine that can:

- Aggregate risk factors
- Calculate risk scores
- Classify risk levels
- Provide explainable risk analysis
- Receive inputs from multiple intelligence domains

---

# 3. Decision

ARPI will implement Risk Intelligence Engine (RIE) as an independent core intelligence module.

RIE will not own market data collection.

RIE will only evaluate standardized intelligence inputs provided by adapters.

---

# 4. RIE Architecture

High-level flow:
Market Engine
|
↓
Market Adapter
|
↓
Risk Intelligence Engine
|
↓
Risk Report
|
↓
Dashboard / Fusion AI
Future architecture:
Market Engine
|
Macro Engine
|
Geopolitical Engine
|
Liquidity Engine
|
↓
Risk Intelligence Engine
|
↓
Fusion AI
---

# 5. Design Principles

## Principle 1 — Independence

RIE must operate independently from any specific data provider.

Incorrect:
Risk Engine
|
↓
Yahoo Finance API
Correct:
Market Provider
|
↓
Market Engine
|
↓
Risk Adapter
|
↓
RIE
---

## Principle 2 — Multi-Dimensional Risk

Risk cannot be evaluated using a single factor.

RIE supports multiple risk dimensions:

- Market Risk
- Volatility Risk
- Macro Risk
- Liquidity Risk
- Geopolitical Risk
- Data Confidence Risk

---

# 6. Risk Input Model

Current RIE input structure:

```json
{
    "market_risk": 0,
    "volatility_risk": 0,
    "macro_risk": 0,
    "liquidity_risk": 0,
    "geopolitical_risk": 0,
    "data_confidence_risk": 0
}
7. Risk Output Model

Standard output:
{
    "asset": "",
    "risk_score": 0,
    "risk_level": "",
    "components": {},
    "confidence": 0,
    "timestamp": ""
}
⸻

8. Risk Classification

Current classification:
0 - 30     LOW

31 - 60    MEDIUM

61 - 80    HIGH

81 - 100   CRITICAL
9. Dashboard Integration Decision

Dashboard must not calculate risk internally.

Previous approach:
Dashboard
     |
     ↓
Market Analysis Risk
New approach:
Dashboard
     |
     ↓
Risk Intelligence Engine
     |
     ↓
Risk Report
10. Current Implementation Status

Completed:

* RIE Core Engine
* Risk Router
* Market Adapter
* Risk API Endpoint
* Dashboard Integration
* Railway Deployment

Production Endpoint:
/risk/analyze/{asset}
11. Future Evolution

RIE v2.0 will support:

* Real Macro Intelligence inputs
* Geopolitical scenarios
* Liquidity analysis
* Historical risk comparison
* Machine learning calibration
* Risk prediction models

⸻

12. Consequences

Positive:

* Independent risk architecture
* Easy integration of future engines
* Explainable decisions
* Enterprise scalability

Trade-offs:

* Requires strict data contracts
* Requires additional adapters
* More initial architecture effort

⸻

Decision Status

ACCEPTED
