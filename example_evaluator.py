from evaluator import Evaluator
from representations import MultiLocationDiseaseTimeSeries, MultiLocationForecast, MultiLocationErrorTimeSeries, \
    ErrorTimeSeries, Error


def mean(samples):
    return sum(samples)/len(samples)

class MAEonMeanPredictions(Evaluator):
    #def evaluate(self, true_values, samples):
    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:
        evaluation_result = MultiLocationErrorTimeSeries(timeseries_dict={})
        for location in all_truths.locations():
            truth_series = all_truths[location]
            forecast_series = all_forecasts.timeseries[location]
            assert len(truth_series.observations) == len(forecast_series.predictions)
            truth_and_forecast_series = zip(truth_series.observations, forecast_series.predictions)
            error = 0
            for truth,prediction in truth_and_forecast_series:
                assert truth.time_period == prediction.time_period, (truth.time_period, prediction.time_period)
                predicted_mean = mean(prediction.disease_case_samples)
                error += abs(truth.disease_cases - predicted_mean)

            mean_absolute_error = error / len(truth_series.observations)
            evaluation_result[location] = ErrorTimeSeries(observations=[Error(time_period="Full_period", value=mean_absolute_error)])
        return evaluation_result
