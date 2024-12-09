from JSON import JSON


class EffectLoader:
    def __init__(self, effect_path):
        self.effect_path = effect_path

    def load(self):
        with open(self.effect_path) as f:
            return f.read()