#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict


import numpy as np
from ax.core.types import TGenMetadata, TParamValue, TParamValueList
from ax.models.base import Model
from ax.models.types import TConfig


class DiscreteModel(Model):
    """This class specifies the interface for a model based on discrete parameters.

    These methods should be implemented to have access to all of the features
    of Ax.
    """

    def fit(
        self,
        Xs: list[list[TParamValueList]],
        Ys: list[list[float]],
        Yvars: list[list[float]],
        parameter_values: list[TParamValueList],
        outcome_names: list[str],
    ) -> None:
        """Fit model to m outcomes.

        Args:
            Xs: A list of m lists X of parameterizations (each parameterization
                is a list of parameter values of length d), each of length k_i,
                for each outcome.
            Ys: The corresponding list of m lists Y, each of length k_i, for
                each outcome.
            Yvars: The variances of each entry in Ys, same shape.
            parameter_values: A list of possible values for each parameter.
            outcome_names: A list of m outcome names.
        """
        pass

    # pyre-fixme[24]: Generic type `np.ndarray` expects 2 type parameters.
    def predict(self, X: list[TParamValueList]) -> tuple[np.ndarray, np.ndarray]:
        """Predict

        Args:
            X: List of the j parameterizations at which to make predictions.

        Returns:
            2-element tuple containing

            - (j x m) array of outcome predictions at X.
            - (j x m x m) array of predictive covariances at X.
              cov[j, m1, m2] is Cov[m1@j, m2@j].
        """
        raise NotImplementedError

    def gen(
        self,
        n: int,
        parameter_values: list[TParamValueList],
        # pyre-fixme[24]: Generic type `np.ndarray` expects 2 type parameters.
        objective_weights: np.ndarray | None,
        # pyre-fixme[24]: Generic type `np.ndarray` expects 2 type parameters.
        outcome_constraints: tuple[np.ndarray, np.ndarray] | None = None,
        fixed_features: dict[int, TParamValue] | None = None,
        pending_observations: list[list[TParamValueList]] | None = None,
        model_gen_options: TConfig | None = None,
    ) -> tuple[list[TParamValueList], list[float], TGenMetadata]:
        """
        Generate new candidates.

        Args:
            n: Number of candidates to generate.
            parameter_values: A list of possible values for each parameter.
            objective_weights: The objective is to maximize a weighted sum of
                the columns of f(x). These are the weights.
            outcome_constraints: A tuple of (A, b). For k outcome constraints
                and m outputs at f(x), A is (k x m) and b is (k x 1) such that
                A f(x) <= b.
            fixed_features: A map {feature_index: value} for features that
                should be fixed to a particular value during generation.
            pending_observations:  A list of m lists of parameterizations
                (each parameterization is a list of parameter values of length d),
                each of length k_i, for each outcome i.
            model_gen_options: A config dictionary that can contain
                model-specific options.

        Returns:
            2-element tuple containing

            - List of n generated points, where each point is represented
              by a list of parameter values.
            - List of weights for each of the n points.
        """
        raise NotImplementedError

    def cross_validate(
        self,
        Xs_train: list[list[TParamValueList]],
        Ys_train: list[list[float]],
        Yvars_train: list[list[float]],
        X_test: list[TParamValueList],
        use_posterior_predictive: bool = False,
        # pyre-fixme[24]: Generic type `np.ndarray` expects 2 type parameters.
    ) -> tuple[np.ndarray, np.ndarray]:
        """Do cross validation with the given training and test sets.

        Training set is given in the same format as to fit. Test set is given
        in the same format as to predict.

        Args:
            Xs_train: A list of m lists X of parameterizations (each parameterization
                is a list of parameter values of length d), each of length k_i,
                for each outcome.
            Ys_train: The corresponding list of m lists Y, each of length k_i, for
                each outcome.
            Yvars_train: The variances of each entry in Ys, same shape.
            X_test: List of the j parameterizations at which to make predictions.
            use_posterior_predictive: A boolean indicating if the predictions
                should be from the posterior predictive (i.e. including
                observation noise).

        Returns:
            2-element tuple containing

            - (j x m) array of outcome predictions at X.
            - (j x m x m) array of predictive covariances at X.
              `cov[j, m1, m2]` is `Cov[m1@j, m2@j]`.
        """
        raise NotImplementedError

    def best_point(
        self,
        n: int,
        parameter_values: list[TParamValueList],
        # pyre-fixme[24]: Generic type `np.ndarray` expects 2 type parameters.
        objective_weights: np.ndarray | None,
        # pyre-fixme[24]: Generic type `np.ndarray` expects 2 type parameters.
        outcome_constraints: tuple[np.ndarray, np.ndarray] | None = None,
        fixed_features: dict[int, TParamValue] | None = None,
        pending_observations: list[list[TParamValueList]] | None = None,
        model_gen_options: TConfig | None = None,
    ) -> TParamValueList | None:
        """Obtains the point that has the best value according to the model
        prediction and its model predictions.

        Returns:
            (1 x d) parameter value list representing the point with the best
            value according to the model prediction. None if this function
            is not implemented for the given model.
        """
        return None
