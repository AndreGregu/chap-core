from evaluator import ComponentBasedEvaluator
from example_component_based_evaluator import mae_error, mean_across_time, mean_across_regions, mse_error, \
    sqrt_mean_across_time
from example_evaluator import MAEonMeanPredictions
from isolated_asses import observations, samples
from representations import MultiLocationErrorTimeSeries

MAE_evaluator = MAEonMeanPredictions()

mae_component_evaluator = ComponentBasedEvaluator("MAE", mae_error, mean_across_time, None)

mae_country_evaluator = ComponentBasedEvaluator("MAE country", mae_error, mean_across_time, mean_across_regions)

absError_timepoint_evaluator = ComponentBasedEvaluator("MAE timpeoint", mae_error, None, None)

rmse_evaluator = ComponentBasedEvaluator("rmse", mse_error, sqrt_mean_across_time, None)

evaluator_suite_options = {
    "onlyLocalMAE": [mae_component_evaluator],
    "localAndGlobalMAE": [mae_component_evaluator, mae_country_evaluator],
    "localMAEandRMSE": [mae_component_evaluator,rmse_evaluator],
    "mix": [mae_component_evaluator,rmse_evaluator,absError_timepoint_evaluator,mae_country_evaluator]
}

class EvaluationPresenter:
    def __init__(self, evaluator_suite):
        self._evaluator_suite = evaluator_suite

    def evaluate_and_present(self, observations, samples):
        print("Results:")
        for evaluator in self._evaluator_suite:
            results : MultiLocationErrorTimeSeries = evaluator.evaluate(observations, samples)
            print(f"***{evaluator.get_name()}***")
            if results.num_locations()==1 and results.num_timeperiods()==1:
                #one value across time and regions
                print(f"{results.get_the_only_location()} - {results.get_the_only_timeseries().observations[0].time_period} : {results.get_the_only_timeseries().observations[0].value}")
            elif results.num_locations()==1:
                #across regions, multiple time points
                raise NotImplementedError("not yes implemented - should be easy")
            elif results.num_timeperiods()==1:
                #multiple regions, aggregated across time
                for region_name, timeseries in results.timeseries_dict.items():
                    print(f"{region_name}: {timeseries.observations[0].value}")
            else:
                #one value per region per time
                print(f"Region\t{'\t'.join([str(t.time_period) for t in list(results.timeseries_dict.values())[0].observations])}")
                for region_name, timeseries in results.timeseries_dict.items():
                    print(f"{region_name}: {'\t'.join([str(t.value) for t in timeseries.observations])}")

chosen_evaluator_euite_key = "mix"
evaluator_suite = evaluator_suite_options[chosen_evaluator_euite_key]
presenter = EvaluationPresenter(evaluator_suite)
presenter.evaluate_and_present(observations, samples)
