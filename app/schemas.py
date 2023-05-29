from typing import List,Dict, Tuple
from pydantic import BaseModel

KPI = Dict[str,float]


class SectionLayoutSchema(BaseModel):
    name:str
    graph : str
    graphKPIs : List[str]


class DashboardLayoutSchema(BaseModel):
  name : str
  cockpit: List[str]
  sections: List[SectionLayoutSchema]


class SectionSchema(SectionLayoutSchema):
   graph_data : List[Tuple[str,float]]
   graphKPIs : List[KPI]


class DashboardSchema(DashboardLayoutSchema):
   cockpit: List[KPI]
   sections: List[SectionSchema]





