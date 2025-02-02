from Minimalist_example.train import train
from Minimalist_example.predict import predict
import pandas as pd

from example_evaluator import MAEonMeanPredictions
from representations import MultiLocationDiseaseTimeSeries, DiseaseTimeSeries, DiseaseObservation, Samples,  Forecast, MultiLocationForecast


def get_arbitrary_sample(predictions_fn):
    df = pd.read_csv(predictions_fn)
    return [Samples(time_period=row.time_period, disease_case_samples=[row.sample_0]) for row in df.itertuples()]


train("Minimalist_example/input/trainData.csv", "Minimalist_example/output/model.bin")
predict("Minimalist_example/output/model.bin", "Minimalist_example/input/trainData.csv", "Minimalist_example/input/futureClimateData.csv", "Minimalist_example/output/predictions.csv")

predictions_fn = "Minimalist_example/output/predictions.csv"
locations = pd.read_csv(predictions_fn)["location"]
assert len(set(locations)) == 1
samples = get_arbitrary_sample(predictions_fn)
assert len(samples)==3

samples = MultiLocationForecast(
    timeseries={locations[0]:
        Forecast(predictions=samples)})

observations = MultiLocationDiseaseTimeSeries(
    timeseries={locations[0]:
        DiseaseTimeSeries(observations=[
            DiseaseObservation(time_period="2023-07", disease_cases=326),
            DiseaseObservation(time_period="2023-08", disease_cases=452),
            DiseaseObservation(time_period="2023-09", disease_cases=453)]) })

mae = MAEonMeanPredictions().evaluate(observations, samples)
print(f"MAE: {mae}")
