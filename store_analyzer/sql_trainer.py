from store_analyzer.base_trainer import BaseTrainer


class SQLTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):
        vn = self.vn
        # Implement SQL training logic here
        vn.train(sql="SELECT first_name, last_name from staff")


if __name__ == "__main__":
    trainer = SQLTrainer()
    trainer.train()
