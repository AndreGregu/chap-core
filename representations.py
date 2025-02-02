from dataclasses import dataclass
from typing import List, Dict


#Disease cases
@dataclass
class DiseaseObservation:
    time_period: str
    disease_cases: int

@dataclass
class DiseaseTimeSeries:
    observations: List[DiseaseObservation]

@dataclass
class MultiLocationDiseaseTimeSeries:
    timeseries: Dict[str,DiseaseTimeSeries]

#Assessment metric
@dataclass
class Error:
    time_period: str
    value: int

@dataclass
class ErrorTimeSeries:
    observations: List[Error]

@dataclass
class MultiLocationErrorTimeSeries:
    timeseries: Dict[str,ErrorTimeSeries]


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
