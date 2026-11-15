import logging
from portfolio_analyzer.ddl_trainer import DDLTrainer
from portfolio_analyzer.doc_trainer import DocTrainer
from portfolio_analyzer.sql_trainer import SQLTrainer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SeedPortfolioAnalyzer")


def seed_all():
    """
    Seeds all DDL, documentation, and SQL query memories for Portfolio Analyzer into Qdrant Cloud.
    """
    logger.info("Step 1/3: Seeding DDL schemas and tables into Qdrant text memory...")
    ddl_trainer = DDLTrainer()
    ddl_trainer.train()

    logger.info("Step 2/3: Seeding domain documentation into Qdrant text memory...")
    doc_trainer = DocTrainer()
    doc_trainer.train()

    logger.info("Step 3/3: Seeding SQL queries into Qdrant tool memory...")
    sql_trainer = SQLTrainer()
    sql_trainer.train()

    logger.info("Portfolio Analyzer memory seeding complete!")


if __name__ == "__main__":
    seed_all()
