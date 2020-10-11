import plotly.graph_objects as go

from src.exploration.erlang_vs_simulation.helpers import compare_number_agents, compare_lambda, \
    compare_aht


def plot_service_levels(x_values: list, erlang_values: list, simulation_values: list):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=erlang_values, name="Erlang")) # line={"width": 10, "color": "black"}
    fig.add_trace(go.Scatter(x=x_values, y=simulation_values, name="Simulation")) # line={"width": 10, "color": "black"}

    return fig


if __name__ == "__main__":
    default_params = {"lambda_": 10, "max_waiting_time": 20, "aht": 180, "aht_sd": 10, "number_agents": 10}
    agents_values = compare_number_agents(default_params, 1, 50, 50)
    lambda_values = compare_lambda(default_params, 3, 6, 50)
    aht_values = compare_aht(default_params, 200, 330, 50)

    plot_service_levels(x_values=agents_values["number_agents"], erlang_values=agents_values["Erlang"],
                        simulation_values=agents_values["Simulation"]).show()

    plot_service_levels(x_values=lambda_values["lambda_"], erlang_values=lambda_values["Erlang"],
                        simulation_values=lambda_values["Simulation"]).show()

    plot_service_levels(x_values=aht_values["aht"], erlang_values=aht_values["Erlang"],
                        simulation_values=aht_values["Simulation"]).show()