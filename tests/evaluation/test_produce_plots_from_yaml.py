from chap_core.plotting.produce_plots_from_yaml import build_from_yaml

YAML_CONFIG = """
configuration:
  - row:
      - plot:
          type: metric
          metric: crps
          plot_type: metric_by_horizon_mean
          title: CRPS by forecast horizon
      - plot:
          type: metric
          metric: crps
          plot_type: metric_by_time_location_mean
"""


def test_plot_titles_from_yaml(flat_observations, flat_forecasts):
    chart = build_from_yaml(
        YAML_CONFIG,
        backtest=None,
        flat_observations=flat_observations,
        flat_forecasts=flat_forecasts,
    )
    first, second = chart.to_dict()["hconcat"]
    assert first["title"] == "CRPS by forecast horizon"
    assert second["title"] == "Mean metric by location and time period"
