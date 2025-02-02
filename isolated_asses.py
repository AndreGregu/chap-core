from chap_core.api_types import PeriodObservation
from chap_core.datatypes import HealthData
from chap_core.spatio_temporal_data.temporal_dataclass import DataSet

from evaluator import ComponentBasedEvaluator
from example_component_based_evaluator import mae_error, mean_across_time
from example_evaluator import MAEonMeanPredictions
from representations import DiseaseObservation, Forecast, MultiLocationDiseaseTimeSeries, DiseaseTimeSeries, Samples, MultiLocationForecast

#Or use HealthData class or HealthObservation class??

observations = MultiLocationDiseaseTimeSeries(
    timeseries={"Oslo":
        DiseaseTimeSeries(observations=[
            DiseaseObservation(time_period="2020-01", disease_cases=0),
            DiseaseObservation(time_period="2020-02", disease_cases=10),
            DiseaseObservation(time_period="2020-03", disease_cases=35)]) })

# truth_dataset = DataSet.from_period_observations(observations)

# samples = {"Oslo": [HealthData(time_period="2020-01", disease_cases=[0,2]),
#     HealthData(time_period="2020-02", disease_cases=[9,13]),
#     HealthData(time_period="2020-03", disease_cases=[31,41])]}

samples = MultiLocationForecast(
    timeseries={"Oslo":
        Forecast(predictions=[
            Samples(time_period="2020-01", disease_case_samples=[0,2]),
            Samples(time_period="2020-02", disease_case_samples=[9,13]),
            Samples(time_period="2020-03", disease_case_samples=[31,41])])})

# samples_dataset = DataSet.from_period_observations(samples)
MAE_evaluator = MAEonMeanPredictions()
mae = MAE_evaluator.evaluate(observations, samples)
print(f"MAE: {mae}")

mae_component_evaluator = ComponentBasedEvaluator(mae_error, mean_across_time, None)
mae2 = mae_component_evaluator.evaluate(observations, samples)
print(f"MAE component-based: {mae2}")