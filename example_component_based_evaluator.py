
def mae_error(truth, predictions):
    return abs(truth - sum(predictions)/len(predictions))

def mean_across_time(errors):
    return sum(errors)/len(errors)

#from evaluate import ComponentBasedEvaluator
#maeComponentEvaluator = ComponentBasedEvaluator(maeError, meanAcrossTime, None)