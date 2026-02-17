from dash import Dash, html, dcc, dash_table, Input, Output, State
from app.models import Team
from app.extensions import db

def init_dash(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/")

    columns = [
        {"name": "ID", "id": "id"},
        {"name": "Nombre", "id": "name"},
        {"name": "Ciudad", "id": "city"},
        {"name": "Estadio", "id": "stadium"},
        {"name": "Año fundación", "id": "founded_year"},
    ]

    dash_app.layout = html.Div(
        style={"maxWidth": "1200px", "margin": "30px auto", "fontFamily": "system-ui"},
        children=[
            html.H2("trabajoFinal — CRUD Premier League 25/26"),
            html.Div(id="msg", style={"marginBottom": "12px"}),

            html.Div(
                style={"display": "flex", "gap": "10px", "flexWrap": "wrap"},
                children=[
                    dcc.Input(id="team_id", placeholder="ID (para actualizar/borrar)", type="number"),
                    dcc.Input(id="name", placeholder="Nombre"),
                    dcc.Input(id="city", placeholder="Ciudad"),
                    dcc.Input(id="stadium", placeholder="Estadio"),
                    dcc.Input(id="founded_year", placeholder="Año fundación", type="number"),
                ],
            ),
            html.Div(
                style={"marginTop": "10px", "display": "flex", "gap": "10px", "flexWrap": "wrap"},
                children=[
                    html.Button("Crear", id="btn_create"),
                    html.Button("Actualizar (por ID)", id="btn_update"),
                    html.Button("Borrar (por ID)", id="btn_delete"),
                    html.Button("Refrescar", id="btn_refresh"),
                ],
            ),

            html.Hr(),
            dash_table.DataTable(
                id="table",
                columns=columns,
                data=[],
                page_size=20,
                sort_action="native",
                filter_action="native",
                style_table={"overflowX": "auto"},
                style_cell={"padding": "8px", "textAlign": "left"},
            ),
        ],
    )

    def fetch_teams():
        # Dash corre dentro de Flask, así que usamos app_context
        with flask_app.app_context():
            teams = Team.query.order_by(Team.name.asc()).all()
            return [t.to_dict() for t in teams]

    @dash_app.callback(
        Output("table", "data"),
        Output("msg", "children"),
        Input("btn_refresh", "n_clicks"),
        prevent_initial_call=False,
    )
    def refresh(_):
        try:
            return fetch_teams(), "✅ Lista actualizada"
        except Exception as e:
            return [], f"❌ Error al cargar: {e}"

    @dash_app.callback(
        Output("msg", "children", allow_duplicate=True),
        Input("btn_create", "n_clicks"),
        State("name", "value"),
        State("city", "value"),
        State("stadium", "value"),
        State("founded_year", "value"),
        prevent_initial_call=True,
    )
    def create(_, name, city, stadium, founded_year):
        try:
            with flask_app.app_context():
                if not name or not str(name).strip():
                    return "❌ Nombre obligatorio"
                t = Team(
                    name=str(name).strip(),
                    city=(str(city).strip() if city else None),
                    stadium=(str(stadium).strip() if stadium else None),
                    founded_year=int(founded_year) if founded_year else None,
                )
                db.session.add(t)
                db.session.commit()
            return "✅ Equipo creado (pulsa Refrescar)"
        except Exception as e:
            return f"❌ Error: {e}"

    @dash_app.callback(
        Output("msg", "children", allow_duplicate=True),
        Input("btn_update", "n_clicks"),
        State("team_id", "value"),
        State("name", "value"),
        State("city", "value"),
        State("stadium", "value"),
        State("founded_year", "value"),
        prevent_initial_call=True,
    )
    def update(_, team_id, name, city, stadium, founded_year):
        if not team_id:
            return "❌ Indica team_id"
        try:
            with flask_app.app_context():
                t = Team.query.get(int(team_id))
                if not t:
                    return "❌ No existe ese ID"

                if name is not None:
                    t.name = str(name).strip()
                if city is not None:
                    t.city = str(city).strip() or None
                if stadium is not None:
                    t.stadium = str(stadium).strip() or None
                if founded_year is not None:
                    t.founded_year = int(founded_year) if founded_year != "" else None

                db.session.commit()
            return "✅ Equipo actualizado (pulsa Refrescar)"
        except Exception as e:
            return f"❌ Error: {e}"

    @dash_app.callback(
        Output("msg", "children", allow_duplicate=True),
        Input("btn_delete", "n_clicks"),
        State("team_id", "value"),
        prevent_initial_call=True,
    )
    def delete(_, team_id):
        if not team_id:
            return "❌ Indica team_id"
        try:
            with flask_app.app_context():
                t = Team.query.get(int(team_id))
                if not t:
                    return "❌ No existe ese ID"
                db.session.delete(t)
                db.session.commit()
            return "✅ Equipo borrado (pulsa Refrescar)"
        except Exception as e:
            return f"❌ Error: {e}"

    return dash_app
