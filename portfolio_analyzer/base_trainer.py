from portfolio_analyzer.common import EnvironmentLoader, MyVanna


class BaseTrainer:
    def __init__(self):
        env_vars = EnvironmentLoader.load_environment_variables()
        self.vn = MyVanna.create_instance(env_vars)

    def get_vn(self):
        return self.vn
