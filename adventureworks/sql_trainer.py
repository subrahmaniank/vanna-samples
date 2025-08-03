from adventureworks.base_trainer import BaseTrainer


class SQLTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):
        vn = self.vn
        # Implement SQL training logic here


if __name__ == "__main__":
    trainer = SQLTrainer()
    trainer.train()
