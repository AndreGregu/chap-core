<<<<<<< HEAD
# Evaluating your model side-by-side with a range of other models

Since Chap integrates a large number of models under a unified interface, it is easy to compare the predictions of your model against those of alternative models using a variety of input data, metrics and visualisations.

The most powerful way of comparing models is to install the Chap modelling platform alongside a DHIS2 instance, allowing you to run your and other models through the GUI of the "Modelling App", which includes interactive side-by-side comparison of predictions by different model.

As a simpler setup, you can also evaluate your own and other models one by one using the [Chap command line interface](running_models_in_chap.md) (the chap evaluate command), and then compare the resulting predictions in your preferred way.
A range of existing models in the field has already been integrated with Chap, and can be run through the Modelling App or by using the [following chap evaluate commands](chap_evaluate_examples.md).
=======
# Evaluating your model side-by-side with a range of other models

Since Chap integrates a large number of models under a unified interface, it is easy to compare the predictions of your model against those of alternative models using a variety of input data, metrics and visualisations.

The most powerful way of comparing models is to install the Chap modelling platform alongside a DHIS2 instance, allowing you to run your and other models through the GUI of the "Modelling App", which includes interactive side-by-side comparison of predictions by different model.

As a simpler setup, you can evaluate your own and other models using the [Chap command line interface](../chap-cli/evaluation-workflow.md) with the `chap eval` command, and then compare the resulting predictions using `chap export-metrics`. See the [Evaluation Workflow](../chap-cli/evaluation-workflow.md) for the recommended approach.

> **Note:** The legacy `chap evaluate` command is deprecated and will be removed in v2.0. See the [legacy examples](chap_evaluate_examples.md) for reference.
>>>>>>> upstream/master
