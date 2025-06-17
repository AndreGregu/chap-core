# CHAP-compatible example of model assessment 
This tutorial provides a guide to and examples of how to do develop a new (custom) evaluation metric that can be used for model evaluation in CHAP.


## Representations of Observations and Predictions
Observations and predictions are each represented using a nested dataclass structure. This design choice reflects the nature of the data: each datapoint connects a specific time period, region, and value (which may be a single value or a set of samples).

To avoid a flat and error-prone representation, and to increase flexibility, the following structure is used:

1. **Datapoint**: Represents a single observation or prediction, containing the time period and data (e.g., a scalar or a list of samples).

2. **TimeSeries**: A dataclass that holds a list of `Datapoint` instances for a single region, ordered by time.

3. **RegionDict**: A dictionary mapping region identifiers to their corresponding `TimeSeries`.


The representation of disease cases and error includes utility methods which streamlines tasks like reordering, transforming, or flattening the data.



An example of the structure for forecast data:
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
The Chap platform can be extended with new (custom) evaluation criteria that based on data in the previously discussed observation and prediction representation defines a new computation according to the evaluator interface found in `evaluator.py`



### The Evaluator interface
For an evaluator to be CHAP-compatible, it needs to implement the evaluate interface defined in the Evaluator abstract class. The abstract class consists of the following two methods:


1. **evaluate**: A method which takes full datastructures for true values and predictions as arguments, and returns a representation of the model’s error. Note that the error data structure can be aggregated over regions or time (does not necessarily contain values for individual regions and time points of the data being evaluated).  
```python
    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:
        pass
```


2. **get_name**: A method which returns the name of the evaluator (to be shown as a name for the defined metric).

```python
    def get_name(self) -> str:
        return self.__class__.__name__
```


#### Example of Evaluator classes
The file `example_evaluator.py` contains an example of a custom evaluator called `MAEonMeanPredictions` which returns the Mean Absolute Error (MAE) for each region across time based on the observed value versus the mean of the prediction samples.


### The generic component-based evaluator
The file `evaluator.py` also includes an Evaluator subclass called `ComponentBasedEvaluator`, which allows to define a new evaluation metric by creating and combining components representing distinct aspects of evaluation. This class is typically used as-is and is not meant to be modified directly. Instead, you define your own custom components that you pass in to its init-method:

- `errorFunc`: a loss function that computes the error between predicted and true values for a single region and time point.

- `timeAggregationFunc`: a function that aggregates errors over time within a single region.

- `regionAggregationFunc`: a function that aggregates the results across regions into a final score.


These components define how the model’s performance is evaluated:

- The **loss function** (`errorFunc`) operates at the individual datapoint or time-step level.

- The **time aggregation function** (`timeAggregationFunc`) summarizes those errors over time for each region.

- The **region aggregation function** (`regionAggregationFunc`) combines the per-region results into a single overall error metric.



This modular approach provides a flexible and reusable evaluation logic. Examples of component functions can be found in `example_component_based_evaluator.py`.



## Evaluator Suites
In many cases, it's useful to evaluate a model using multiple complementary error metrics simultaneously. Additionally, how these metrics are presented can vary depending on the use case. To support this, we use **evaluator suites** — collections of evaluators grouped in a dictionary and processed together.

The class `EvaluationPresenter` in `example_evaluator_suites.py` demonstrates how to run several evaluators at once and present their results in a structured and readable format. The example also shows how to define multiple suites, allowing users to choose between predefined sets of evaluators depending on their evaluation needs.

This design makes it easy to compare models using a variety of metrics and presentation formats with minimal changes to the code.


## Evaluating on real data
This repository also includes a few illustrative examples of how to use this format to evaluate models trained on real data. For real usage with Chap, see a separate documentation of how an evaluation metric defined according to the interfaces described here (that follows the Evaluator abstract class) can be easily integrated into Chap and used as metric for any evaluation performed in that platform.


### Evaluating `minimalist_example` with custom evaluator
The file `asses_minimalist.py` is an extension of `asses_minimalist.py` from `Assessment_example_singlepred` which now uses a subclass of Evaluator to evaluate with MAE. 


### Evaluating `minimalist_example` with evaluator suite
In `example_evaluator_suites.py` it is shown an example of how to use evaluator suites and the `EvaluationPresenter` class to assess the same model and data from `minimalist_example`. The different evaluators are made from the `ComponentBasedEvaluator`.
