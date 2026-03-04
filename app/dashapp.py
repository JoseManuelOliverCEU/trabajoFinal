from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context, no_update
from flask_login import login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app.models import Team, User
from app.extensions import db


def init_dash(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/")
    dash_app.config.suppress_callback_exceptions = True

    columns = [
        {"name": "ID", "id": "id"},
        {"name": "Nombre", "id": "name"},
        {"name": "Ciudad", "id": "city"},
        {"name": "Estadio", "id": "stadium"},
        {"name": "Año fundación", "id": "founded_year"},
    ]

    # -----------------------------
    # Builders (to "remount" login)
    # -----------------------------
    def build_login_children():
        # Remontar inputs evita que queden valores en memoria.
        # autoComplete off/new-password reduce muchísimo el autofill.
        return [
            html.H3("Login"),
            html.Div(
                className="row",
                children=[
                    dcc.Input(
                        id="login_user",
                        placeholder="Usuario",
                        debounce=True,
                        value="",
                        autoComplete="off",
                        inputMode="text",
                    ),
                    dcc.Input(
                        id="login_pass",
                        placeholder="Contraseña",
                        type="password",
                        debounce=True,
                        value="",
                        autoComplete="new-password",
                    ),
                    html.Button("Entrar", id="btn_login"),
                ],
            ),
        ]

    def fetch_teams():
        with flask_app.app_context():
            teams = Team.query.order_by(Team.name.asc()).all()
            return [t.to_dict() for t in teams]

    def render_admin_crud():
        return html.Div(
            className="row",
            children=[
                dcc.Input(id="team_id", placeholder="ID", type="number"),
                dcc.Input(id="name", placeholder="Nombre"),
                dcc.Input(id="city", placeholder="Ciudad"),
                dcc.Input(id="stadium", placeholder="Estadio"),
                dcc.Input(id="founded_year", placeholder="Año fundación", type="number"),
                html.Button("Crear", id="btn_create"),
                html.Button("Actualizar", id="btn_update", className="secondary"),
                html.Button("Borrar", id="btn_delete", className="danger"),
            ],
        )

    # -----------------------------
    # Layout
    # -----------------------------
    dash_app.layout = html.Div(
        className="container",
        children=[
            dcc.Location(id="url"),
            dcc.Store(id="auth", storage_type="session"),

            html.Div(
                className="header",
                children=[
                    html.H2("trabajoFinal — Premier League 25/26", className="title"),
                    html.Div(id="whoami", className="badge"),
                ],
            ),

            html.Div(id="msg", className="msg"),

            # LOGIN CARD
            html.Div(
                id="login_box",
                className="card",
                children=build_login_children(),
                style={"display": "block"},
            ),

            # MAIN CARD
            html.Div(
                id="main_box",
                className="card",
                children=[
                    html.Div(
                        className="row",
                        children=[
                            html.Button("Cerrar sesión", id="btn_logout", className="ghost"),
                            html.Button("Refrescar", id="btn_refresh", className="secondary"),
                        ],
                    ),
                    html.Div(id="crud_box", style={"marginTop": "15px"}),
                    html.Hr(),
                    dash_table.DataTable(
                        id="table",
                        columns=columns,
                        data=[],
                        page_size=20,
                        sort_action="native",
                        filter_action="native",
                        style_table={"overflowX": "auto"},
                        style_cell={"padding": "10px", "textAlign": "left"},
                    ),
                ],
                style={"display": "none"},
            ),
        ],
    )

    # -----------------------------
    # AUTH FLOW
    # -----------------------------
    @dash_app.callback(
        Output("auth", "data"),
        Output("msg", "children"),
        Output("login_box", "style"),
        Output("main_box", "style"),
        Output("crud_box", "children"),
        Output("whoami", "children"),
        Output("table", "data"),
        Output("login_box", "children"),   # <- CLAVE: remonta login para borrar credenciales
        Input("url", "pathname"),
        Input("btn_login", "n_clicks"),
        Input("btn_logout", "n_clicks"),
        State("login_user", "value"),
        State("login_pass", "value"),
        prevent_initial_call=False,
    )
    def auth_flow(_pathname, _n_login, _n_logout, username, password):
        trig = callback_context.triggered_id

        # Al cargar la página: SIEMPRE mostramos login (sin sesión)
        if trig == "url" or trig is None:
            logout_user()
            return (
                {"authed": False, "role": None},
                "",
                {"display": "block"},
                {"display": "none"},
                "",
                "",
                [],
                build_login_children(),   # <- inputs vacíos
            )

        # Logout: borrar sesión + borrar credenciales del formulario
        if trig == "btn_logout":
            logout_user()
            return (
                {"authed": False, "role": None},
                "Sesión cerrada",
                {"display": "block"},
                {"display": "none"},
                "",
                "",
                [],
                build_login_children(),   # <- inputs vacíos (no queda nada escrito)
            )

        # Login
        if trig == "btn_login":
            if not username or not password:
                return (
                    no_update,
                    "Usuario y contraseña obligatorios",
                    no_update, no_update, no_update, no_update, no_update,
                    no_update
                )

            with flask_app.app_context():
                u = User.query.filter_by(username=str(username).strip()).first()

                if not u or not u.check_password(str(password)):
                    # Por seguridad, también “reseteamos” el login para borrar password
                    return (
                        no_update,
                        "Credenciales inválidas",
                        {"display": "block"},
                        {"display": "none"},
                        "",
                        "",
                        [],
                        build_login_children(),
                    )

                login_user(u)

                role = (u.role or "user").strip().lower()
                teams = fetch_teams()
                crud = render_admin_crud() if role == "admin" else html.Div()

                return (
                    {"authed": True, "role": role},
                    f"Bienvenido {u.username} ({role})",
                    {"display": "none"},
                    {"display": "block"},
                    crud,
                    f"{u.username} ({role})",
                    teams,
                    no_update,  # <- no hace falta reconstruir login aquí
                )

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # -----------------------------
    # REFRESH TABLE (only if authed)
    # -----------------------------
    @dash_app.callback(
        Output("table", "data", allow_duplicate=True),
        Output("msg", "children", allow_duplicate=True),
        Input("btn_refresh", "n_clicks"),
        State("auth", "data"),
        prevent_initial_call=True,
    )
    def refresh(_n, auth):
        if not auth or not auth.get("authed"):
            return no_update, "Debes iniciar sesión"
        try:
            return fetch_teams(), "✅ Lista actualizada"
        except Exception as e:
            return no_update, f"❌ Error al refrescar: {e}"

    # -----------------------------
    # CREATE (admin only)
    # -----------------------------
    @dash_app.callback(
        Output("msg", "children", allow_duplicate=True),
        Input("btn_create", "n_clicks"),
        State("auth", "data"),
        State("name", "value"),
        State("city", "value"),
        State("stadium", "value"),
        State("founded_year", "value"),
        prevent_initial_call=True,
    )
    def create(_n, auth, name, city, stadium, founded_year):
        if not auth or auth.get("role") != "admin":
            return "No autorizado"

        if not name or not str(name).strip():
            return "Nombre obligatorio"

        try:
            with flask_app.app_context():
                t = Team(
                    name=str(name).strip(),
                    city=(str(city).strip() if city else None),
                    stadium=(str(stadium).strip() if stadium else None),
                    founded_year=int(founded_year) if founded_year else None,
                )
                db.session.add(t)
                db.session.commit()
            return "✅ Equipo creado (pulsa Refrescar)"
        except IntegrityError:
            db.session.rollback()
            return "❌ El equipo ya existe"
        except Exception as e:
            db.session.rollback()
            return f"❌ Error: {e}"

    # -----------------------------
    # UPDATE (admin only)
    # -----------------------------
    @dash_app.callback(
        Output("msg", "children", allow_duplicate=True),
        Input("btn_update", "n_clicks"),
        State("auth", "data"),
        State("team_id", "value"),
        State("name", "value"),
        State("city", "value"),
        State("stadium", "value"),
        State("founded_year", "value"),
        prevent_initial_call=True,
    )
    def update(_n, auth, team_id, name, city, stadium, founded_year):
        if not auth or auth.get("role") != "admin":
            return "No autorizado"

        if not team_id:
            return "Indica un ID"

        with flask_app.app_context():
            t = Team.query.get(int(team_id))
            if not t:
                return "❌ Equipo no encontrado"

            if name is not None:
                t.name = str(name).strip()
            if city is not None:
                t.city = str(city).strip() or None
            if stadium is not None:
                t.stadium = str(stadium).strip() or None
            if founded_year is not None:
                fy = str(founded_year).strip()
                t.founded_year = int(fy) if fy != "" else None

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return "❌ Otro equipo ya tiene ese nombre"
            except Exception as e:
                db.session.rollback()
                return f"❌ Error: {e}"

        return "✅ Equipo actualizado (pulsa Refrescar)"

    # -----------------------------
    # DELETE (admin only)
    # -----------------------------
    @dash_app.callback(
        Output("msg", "children", allow_duplicate=True),
        Input("btn_delete", "n_clicks"),
        State("auth", "data"),
        State("team_id", "value"),
        prevent_initial_call=True,
    )
    def delete(_n, auth, team_id):
        if not auth or auth.get("role") != "admin":
            return "No autorizado"

        if not team_id:
            return "Indica un ID"

        with flask_app.app_context():
            t = Team.query.get(int(team_id))
            if not t:
                return "❌ Equipo no encontrado"
            db.session.delete(t)
            db.session.commit()

        return "✅ Equipo eliminado (pulsa Refrescar)"

    return dash_app