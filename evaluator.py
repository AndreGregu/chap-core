from representations import MultiLocationDiseaseTimeSeries, MultiLocationForecast, \
    MultiLocationErrorTimeSeries, ErrorTimeSeries, Error

from abc import ABC, abstractmethod

# class Evaluator(ABC):
#     @abstractmethod
#     def evaluate(self, truth: DataSet, all_forecasts: dict[str, DataSet[Samples]], ) -> dict[str, DataSet[float]]:
#         pass

class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:
        pass

    def get_name(self) -> str:
        return self.__class__.__name__


class ComponentBasedEvaluator(Evaluator):
    def __init__(self, name, errorFunc, timeAggregationFunc, regionAggregationFunc):
        self._name = name
        self._errorFunc = errorFunc
        self._timeAggregationFunc = timeAggregationFunc
        self._regionAggregationFunc = regionAggregationFunc

    def get_name(self):
        return self._name

    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:

        evaluation_result = MultiLocationErrorTimeSeries(timeseries={})
        all_error_series = []
        for location in all_truths.timeseries:
            current_error_series = ErrorTimeSeries(observations=[])
            truth_series = all_truths.timeseries[location]
            forecast_series = all_forecasts.timeseries[location]
            assert len(truth_series.observations) == len(forecast_series.predictions)
            truth_and_forecast_series = zip(truth_series.observations, forecast_series.predictions)
            errors = []
            for truth,prediction in truth_and_forecast_series:
                assert truth.time_period == prediction.time_period
                errors.append( self._errorFunc(truth.disease_cases, prediction.disease_case_samples) )
                if self._timeAggregationFunc is None:
                    current_error_series.observations.append(Error(time_period=truth.time_period, value=errors[-1]))
            if self._timeAggregationFunc is not None:
                current_error_series.observations.append(Error(time_period="Full_period",
                    value=self._timeAggregationFunc(errors)))
            if self._regionAggregationFunc is None:
                evaluation_result.timeseries[location] = current_error_series
            else:
                all_error_series.append(current_error_series)
        if self._regionAggregationFunc is not None:
            across_regions = zip(*[s.observations for s in all_error_series])
            error_across_regions = [Error(time_period=timepoint_errors[0].time_period,
                   value=self._regionAggregationFunc([e.value for e in timepoint_errors])) \
             for timepoint_errors in across_regions]
            evaluation_result.timeseries["Full_region"] = ErrorTimeSeries(observations=error_across_regions)

        return evaluation_result

