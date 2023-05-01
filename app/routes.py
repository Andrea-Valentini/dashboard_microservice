from app import app, db
from flask import jsonify
from app.models import Section,Component, Dashboard
from app.functions import get_dashboard_layout, get_kpi_value, get_graph_data
from pydantic import BaseModel
from typing import List
from flask_pydantic import validate

class CreateDashboard(BaseModel):
  dashboard_name : str
  cockpit: List[str]
  sectionList: List[dict]


class GetDashboard(BaseModel):
  dashboard_name: str

@app.route('/create_dashboard', methods = ["POST"])
@validate()
def create_dashboard(body:CreateDashboard):

    dashboard_name = body.dashboard_name
    dashboard_model = Dashboard(name=dashboard_name)
    db.session.add(dashboard_model)

    cockpit = body.cockpit
    section_model = Section(name="cockpit",dashboard = dashboard_model)
    db.session.add(section_model)


    for kpi in cockpit:
        component_model = Component(code=kpi, section=section_model)
        db.session.add(component_model)
        

    for section in body.sectionList:

        section_model = Section(name=next(iter(section)),dashboard = dashboard_model)
        db.session.add(section_model)

        for component in section.values():   
            graph_component_model = Component(code=component["graph"], section=section_model)
            db.session.add(graph_component_model)
            
            for kpi in component["graphKPIs"]:
                sub_component_model = Component(code=kpi, section=section_model, component=graph_component_model)
                db.session.add(sub_component_model)

    db.session.commit()

    return "", 201


@app.route('/get_dashboard', methods = ["GET"])
@validate()
def get_dashboard(query:GetDashboard):

    dashboard_name = query.dashboard_name

    dashboard = Dashboard.query.filter_by(name=dashboard_name).first()

    if not dashboard:
        return jsonify({"message":"not found"}), 404
    
    return jsonify(get_dashboard_layout(dashboard)) , 200

@app.route('/get_dashboard_data', methods = ["GET"])
@validate()
def get_dashboard_data(query:GetDashboard):

    dashboard_name = query.dashboard_name
    dashboard = Dashboard.query.filter_by(name=dashboard_name).first()

    if not dashboard:
        return jsonify({"message":"not found"}), 404
    
    dashboard_layout_dict = get_dashboard_layout(dashboard)


    cockpit_list = []

    for kpi in dashboard_layout_dict["cockpit"]:
        cockpit_list.append({kpi:get_kpi_value(kpi)})

    Section_list = []
    for section in dashboard_layout_dict["sectionList"]:


        section_name = next(iter(section))
        graph = section[section_name]["graph"]
        section_dict={}
        section_dict["graph_data"] = {graph:get_graph_data(graph)}
        section_dict["graphKPIs"] = []
        section_dict["graph_name"] = section_name


        for kpi in section[section_name]["graphKPIs"]:
            section_dict["graphKPIs"].append({kpi:get_kpi_value(kpi)})

        Section_list.append(section_dict)
    
    results={
        "dashboard_name":dashboard_name,
        "cockpit":cockpit_list,
        "sectionList":Section_list
    }
    

    return jsonify(results),200 
