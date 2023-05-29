from app import app, db
from flask import jsonify
from app.models import Section, Component, Dashboard
from app.functions import get_dashboard_layout, get_kpi_value, get_graph_data
from flask_pydantic import validate
from app.schemas import DashboardLayoutSchema, SectionSchema, DashboardSchema


@app.route("/dashboard", methods=["POST"])
@validate()
def create_dashboard(body: DashboardLayoutSchema):
    dashboard_model = Dashboard(name=body.name)
    db.session.add(dashboard_model)

    cockpit = body.cockpit
    section_model = Section(name="cockpit", dashboard=dashboard_model)
    db.session.add(section_model)

    for kpi in cockpit:
        component_model = Component(code=kpi, section=section_model)
        db.session.add(component_model)

    for section in body.sections:
        section_model = Section(name=section.name, dashboard=dashboard_model)
        db.session.add(section_model)

        graph_component_model = Component(code=section.graph, section=section_model)
        db.session.add(graph_component_model)

        for kpi in section.graphKPIs:
            kpi_component_model = Component(
                code=kpi, section=section_model, component=graph_component_model
            )
            db.session.add(kpi_component_model)

    db.session.commit()

    return "", 201


@app.route("/dashboard/<id>", methods=["GET"])
@validate()
def get_dashboard(id: int):
    dashboard = Dashboard.query.filter_by(id=int(id)).first()

    if not dashboard:
        return jsonify({"message": "not found"}), 404

    return get_dashboard_layout(dashboard), 200


@app.route("/dashboard/<id>/data", methods=["GET"])
@validate()
def get_dashboard_data(id: int):
    dashboard = Dashboard.query.filter_by(id=int(id)).first()

    if not dashboard:
        return jsonify({"message": "not found"}), 404

    dashboard_layout = get_dashboard_layout(dashboard)

    cockpit_list = []

    for kpi in dashboard_layout.cockpit:
        cockpit_list.append({kpi: get_kpi_value(kpi)})

    section_list = []

    for section_layout in dashboard_layout.sections:
        section = SectionSchema(
            name=section_layout.name,
            graph=section_layout.graph,
            graph_data=get_graph_data(section_layout.graph),
            graphKPIs=[{kpi: get_kpi_value(kpi)} for kpi in section_layout.graphKPIs],
        )

        section_list.append(section)

    return (
        DashboardSchema(
            name=dashboard.name,
            cockpit=[{kpi: get_kpi_value(kpi)} for kpi in dashboard_layout.cockpit],
            sections=section_list,
        ),
        200,
    )
