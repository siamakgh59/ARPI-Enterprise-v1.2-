from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ARPIIntelligenceContract(BaseModel):
    """
    Central Intelligence Contract for ARPI Enterprise.

    This contract provides a common interface between:
    - Market Engine
    - Gold Intelligence Engine
    - Macro Intelligence Engine
    - Risk Intelligence Engine
    - Fusion Engine
    - Reasoning Engine
    - Orchestrator Layer
    """

    # =========================
    # Identity
    # =========================

    engine: str

    version: str

    domain: str

    asset: Optional[str] = None

    # =========================
    # Intelligence
    # =========================

    score: Optional[float] = None

    risk_score: Optional[float] = None

    risk_level: Optional[str] = None

    signal: Optional[str] = None

    trend: Optional[str] = None

    confidence: float = 0

    # =========================
    # Intelligence Explanation
    # =========================

    drivers: List[str] = Field(
        default_factory=list
    )

    risks: List[str] = Field(
        default_factory=list
    )

    warnings: List[str] = Field(
        default_factory=list
    )

    # =========================
    # Data Quality
    # =========================

    data_quality: str = "UNKNOWN"

    available_inputs: int = 0

    missing_inputs: List[str] = Field(
        default_factory=list
    )

    # =========================
    # Additional Metadata
    # =========================

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    # =========================
    # Timestamp
    # =========================

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )
