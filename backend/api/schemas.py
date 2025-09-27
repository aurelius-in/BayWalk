from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class Scene(BaseModel):
    anchors: List[Dict[str, Any]] = Field(default_factory=list)
    zones: List[Dict[str, Any]] = Field(default_factory=list)


class Placement(BaseModel):
    id: str
    x: float
    y: float
    z: float
    lens: str


class CoverageResult(BaseModel):
    pct: float
    blind_spots: int
    placements: List[Placement]


class EdgeProfile(BaseModel):
    type: str
    gpu_mem_gb: int
    thermal_ok: bool
    total_fps: Optional[float] = None


class PowerBudget(BaseModel):
    budget_w: float
    switch: str
    cams: int


class Route(BaseModel):
    cam_id: str
    to: Dict[str, float]
    length_m: float


class RoutingResult(BaseModel):
    total_length_m: float
    paths: List[Route]


class BOMItem(BaseModel):
    sku: str
    qty: int
    unit_usd: float
    desc: str | None = None


class BOM(BaseModel):
    total_usd: float
    items: List[BOMItem]


class PolicyResult(BaseModel):
    allow: bool
    checks: List[str] | None = None


class CostResult(BaseModel):
    estimated_total_usd: float


class JiraBundle(BaseModel):
    epics: List[Dict[str, Any]]
    stories: List[Dict[str, Any]]


class Artifacts(BaseModel):
    kit_ready: bool


class PlanResponse(BaseModel):
    project_id: str
    coverage: CoverageResult
    edge_profile: EdgeProfile
    power: PowerBudget
    routes: RoutingResult
    bom: BOM
    policies: PolicyResult
    costs: CostResult
    messages: List[str]
