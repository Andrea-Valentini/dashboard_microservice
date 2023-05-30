from app.models import Trades, CalculatedTrades, CalculatedMarketTrades, Dashboard
from app.constants import (
    DataTrades,
    CalculatedDataMarketTrades,
    Timescale,
    Operation,
    CalculatedDataTrades,
)
from app.schemas import DashboardLayoutSchema, SectionLayoutSchema
from app.db import db
from sqlalchemy import extract, func


def get_dashboard_layout(dashboard: Dashboard) -> DashboardLayoutSchema:
    sections = dashboard.sections

    sectionsList = cockpit = []

    for section in sections:
        components = section.components

        if section.name == "cockpit":
            cockpit = [component.code for component in components]
            continue

        else:
            graphKPIs = []

            for component in components:
                if component.component_id is None:
                    graph = component.code
                else:
                    graphKPIs.append(component.code)

        sectionsList.append(
            SectionLayoutSchema(name=section.name, graph=graph, graphKPIs=graphKPIs)
        )

    return DashboardLayoutSchema(
        name=dashboard.name, cockpit=cockpit, sections=sectionsList
    )


def get_timescale(timescale):
    if timescale == Timescale.YEARLY.value:
        return "year"

    if timescale == Timescale.MONTHLY.value:
        return "month"

    if timescale == Timescale.DAILY.value:
        return "day"


def get_model(data):
    if data in DataTrades:
        return Trades

    if data in CalculatedDataTrades:
        return CalculatedTrades

    if data in CalculatedDataMarketTrades:
        return CalculatedMarketTrades


def get_cumulated_values(timescale, data):
    model = get_model(data)
    timescale = get_timescale(timescale)
    timescale = extract(timescale, getattr(model, "timestamp"))

    results = db.session.query(
        func.sum(getattr(model, data)).label("cumulative")
    ).group_by(timescale)

    return results


def get_cumulated_kpi(timescale, data):
    return get_cumulated_values(timescale, data).first()[0]


def get_lastdiff_kpi(timescale, data):
    first, second = get_cumulated_values(timescale, data).limit(2).all()

    return (first[0] - second[0]) / first[0] * 100


def get_avg_kpi(timescale, data):
    model = get_model(data)
    timescale = get_timescale(timescale)
    timescale = extract(timescale, getattr(model, "timestamp"))
    results = db.session.query(
        func.avg(getattr(model, data)).label("average")
    ).group_by(timescale)

    return results.first()


def get_kpi_value(kpi):
    data, operation, timescale = kpi.split("-")

    if operation == Operation.CUMULATE.value:
        return get_cumulated_kpi(timescale, data)

    if operation == Operation.LASTDIFF.value:
        return get_lastdiff_kpi(timescale, data)

    if operation == Operation.AVERAGE.value:
        return get_avg_kpi(timescale, data)[0]


def get_graph_data(data):
    model = get_model(data)
    res = db.session.query(getattr(model, "timestamp"), getattr(model, data)).all()

    return list(
        map(lambda r: (r[0].strftime(format="%Y-%b-%d %H:%M:%S"), str(r[1])), res)
    )
