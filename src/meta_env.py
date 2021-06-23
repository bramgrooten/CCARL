from gym import Wrapper
import numpy as np
from src.context_changer import add_gaussian_noise

class MetaEnv(Wrapper):
    def __init__(
            self,
            env,
            contexts,
            instance_mode="rr",
            hide_context=False,
            add_gaussian_noise_to_context: bool = True,
            gaussian_noise_std_percentage: float = 0.01
    ):
        super().__init__(env=env)
        self.contexts = contexts
        self.instance_mode = instance_mode
        self.hide_context = hide_context
        self.context = contexts[0]
        self.context_index = 0

        self.add_gaussian_noise_to_context = add_gaussian_noise_to_context
        self.gaussian_noise_std_percentage = gaussian_noise_std_percentage
        self.whitelist_gaussian_noise = None  # type: list[str]

    def reset(self):
        self._progress_instance()
        self._update_context()
        state = self.env.reset()
        if not hide_context:
            state = np.concatenate(state, np.array(list(self.context.values())))
        return state

    def step(self, action):
        state, reward, done, info = self.env.step(action)
        if not hide_context:
            state = np.concatenate(state, np.array(list(self.context.values())))
        return state, reward, done, info

    def __getattr__(self, name):
        if name in ["_progress_instance", "_update_context"]:
            return getattr(self, name)
        if name.startswith('_'):
            raise AttributeError("attempted to get missing private attribute '{}'".format(name))
        return getattr(self.env, name)

    def _progress_instance(self):
        if self.instance_mode == "random":
            self.context_index = np.random_choice(np.arange(len(self.contexts.keys())))
        else:
            self.context_index = (self.context_index + 1) % len(self.contexts.keys())
        self.context = self.contexts[self.context_index]

        # TODO use class for context changing / value augmentation
        if self.add_gaussian_noise_to_context and self.whitelist_gaussian_noise:
            for key, value in self.context.items():
                if key in self.whitelist_gaussian_noise:
                    self.context[key] = add_gaussian_noise(
                        default_value=value,
                        percentage_std=self.gaussian_noise_std_percentage,
                        random_generator=self.np_random
                    )

    def _update_context(self):
        raise NotImplementedError


