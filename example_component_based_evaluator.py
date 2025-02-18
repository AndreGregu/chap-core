import math


def mae_error(truth : float, predictions : list[float]):
    return abs(truth - sum(predictions)/len(predictions))

def mean_across_time(errors):
    return sum(errors)/len(errors)

def mean_across_regions(errors):
    return sum(errors) / len(errors)
def mse_error(truth : float, predictions : list[float]):
    return (truth - sum(predictions)/len(predictions))**2

def sqrt_mean_across_time(errors):
    return math.sqrt(sum(errors)/len(errors) )

#from evaluate import ComponentBasedEvaluator
#maeComponentEvaluator = ComponentBasedEvaluator(maeError, meanAcrossTime, None)