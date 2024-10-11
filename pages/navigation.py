import dash_bootstrap_components as dbc
from dash import html
from app import app

navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url('bullish.png'), height="30px"),
                dbc.NavbarBrand("FinSight", className="ms-2"),
            ],
            width= {"size":"auto"})
        ],
        align = "center",
        className = "g-0"
        ),
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Home", href="/")),
                    dbc.NavItem(dbc.NavLink("Visualize", href="/visualize")),
                    dbc.NavItem(dbc.NavLink("Forecasting" , href="/forecasting")),
                    dbc.NavItem(dbc.NavLink("News" , href="/news")),
                    dbc.NavItem(dbc.NavLink("About" , href="/about"))    
                ],
                navbar = True, 
                )
                
            ],
            width= {"size":"auto"}
            )
        ],
        align = "center")
 ]),
    color="primary",
    dark=True,
)