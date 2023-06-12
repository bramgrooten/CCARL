from __future__ import annotations

import numpy as np

from carl.context.context_space import ContextFeature, UniformFloatContextFeature
from carl.envs.gymnasium.carl_gymnasium_env import CARLGymnasiumEnv


class CARLCartPole(CARLGymnasiumEnv):
    env_name: str = "CartPole-v1"

    def _update_context(self) -> None:
        for k, v in self.context.items():
            setattr(self.env, k, v)

    def get_context_features() -> list[ContextFeature]:
        return {
            "gravity": UniformFloatContextFeature(
                "gravity", lower=0.1, upper=np.inf, default_value=9.8
            ),
            "masscart": UniformFloatContextFeature(
                "masscart", lower=0.1, upper=10, default_value=1.0
            ),
            "masspole": UniformFloatContextFeature(
                "masspole", lower=0.01, upper=1, default_value=0.1
            ),
            "length": UniformFloatContextFeature(
                "length", lower=0.05, upper=5, default_value=0.5
            ),
            "force_mag": UniformFloatContextFeature(
                "force_mag", lower=1, upper=100, default_value=10.0
            ),
            "tau": UniformFloatContextFeature(
                "tau", lower=0.002, upper=0.2, default_value=0.02
            ),
        }
