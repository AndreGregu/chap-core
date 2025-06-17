# CHAP-compatible example of model assessment 
This tutorial provides a guide to and examples of how to do model assessment in CHAP with user-defined evaluation criteria in python.


## Representations of Observations and Predictions
Observations and predictions are represented using a nested dataclass structure. This design choice reflects the nature of the data: each datapoint is associated with a specific time period, region, and value (which may be a single value or a set of samples).

To avoid a flat and error-prone representation, and to increase flexibility, the following structure is used:

1. **Datapoint**: Represents a single observation or prediction, containing the time period and data (e.g., a scalar or a list of samples).

2. **TimeSeries**: A dataclass that holds a list of `Datapoint` instances for a single region, ordered by time.

3. **RegionDict**: A dictionary mapping region identifiers to their corresponding `TimeSeries`.


The representation of diseasecases and error includes utility methods which also allows for supports tasks like reordering, transforming, or flattening the data.



An example of the structure for forcast data:
```python

#Forecasts

@dataclass
class Samples:
    time_period: str
    disease_case_samples: List[float]


@dataclass
class Forecast:
    predictions: List[Samples]


@dataclass
class MultiLocationForecast:
    timeseries: Dict[str,Forecast]
```


## Isolated assessment example using this data-representation
Before getting a new model to work as part of CHAP, it can be useful to develop and debug it while running it directly a small dataset.


The example can be run in isolation (e.g. from the command line) using the file isolated_asses.py:
```bash
python isolated_asses.py

```

The example uses arbitrary disease data and predictions in the nested format, then applies multiple predefined evaluators to compute various error metrics.



## Manually writing custom evaluators
Sometimes one would want to define some custom evaluation criteria. This is possible in CHAP using the previously discussed observation and prediction representation and the evaluator interface found in `evaluator.py`



### The Evaluator interface
For an evaluator to be CHAP-compatible, it needs to be a instance of the Evaluator abstract class. The abstract class consists of the following two methods:


1. **evaluate**: A method which takes true values and predictions as arguments, and returns a representation of the model’s error. 
```python
    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:
        pass
```


2. **get_name**: A method which returns the name of the evaluator

```python
    def get_name(self) -> str:
        return self.__class__.__name__
```


#### Example of Evaluator classes
The file `example_evaluator.py` contains an example of a custom evaluator called `MAEonMeanPredictions` which returns the Mean Absolute Error (MAE) for each region based on the mean of the prediction samples.


### The generic component-based evaluator
In the file `evaluator.py` it is also included an Evaluator subclass called `ComponentBasedEvaluator`. This class is typically used as-is and is not meant to be modified directly. Instead, you define your own custom components:

- `errorFunc`: a loss function that computes the error between predicted and true values.

- `timeAggregationFunc`: a function that aggregates errors over time within a single region.

- `regionAggregationFunc`: a function that aggregates the results across regions into a final score.


These components define how the model’s performance is evaluated:

- The **loss function** (`errorFunc`) operates at the individual datapoint or time-step level.

- The **time aggregation function** (`timeAggregationFunc`) summarizes those errors over time for each region.

- The **region aggregation function** (`regionAggregationFunc`) combines the per-region results into a single overall error metric.



This modular approach provides a flexible and reusable evaluation logic. Examples of component functions can be found in `example_component_based_evaluator.py`.



## Evaluator Suites
In many cases, it's useful to evaluate a model using multiple error metrics simultaneously. Additionally, how these metrics are presented can vary depending on the use case. To support this, we use **evaluator suites** — collections of evaluators grouped in a dictionary and processed together.

The class `EvaluationPresenter` in `example_evaluator_suites.py` demonstrates how to run several evaluators at once and present their results in a structured and readable format. The example also shows how to define multiple suites, allowing users to choose between predefined sets of evaluators depending on their evaluation needs.

This design makes it easy to compare models using a variety of metrics and presentation formats with minimal changes to the code.


## Evaluating on real data
We have also included some examples of how to use this format to evaluate models trained on real data. 


### Evaluating `minimalist_example` with custom evaluator
The file `asses_minimalist.py` is an extension of `asses_minimalist.py` from `Assessment_example_singlepred` which now uses a subclass of Evaluator to evaluate with MAE. 


### Evaluating `minimalist_example` with evaluator suite
In `example_evaluator_suites.py` it is shown an example of how to use evaluator suites and the `EvaluationPresenter` class to assess the same model and data from `minimalist_example`. The different evaluators are made from the `ComponentBasedEvaluator`.
