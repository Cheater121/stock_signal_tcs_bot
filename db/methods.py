from datetime import datetime

from db.models import Stock, Indicator, database
from errors.setup_logger import logger


class DatabaseConnector:
    def __init__(self, db):
        self.db = db

    def _create_tables(self):
        try:
            self.db.connect()
            self.db.create_tables([Stock, Indicator])
        except Exception as e:
            logger.exception(f"Exception in create tables method: \n{e}\n")
        finally:
            self.db.close()

    def _save_or_get_stock(self, ticker: str, figi: str):
        try:
            self._create_tables()
            self.db.connect()
            stock, create = Stock.get_or_create(ticker=ticker, figi=figi)
            logger.info(f"Stock '{ticker}' saved successfully.")
            return stock, create
        except Exception as e:
            logger.exception(f"Exception in save stock method: \n{e}\n")
        finally:
            self.db.close()

    def save_old_prices(self, ticker: str, figi: str, old_levels: dict):
        try:
            stock, *_ = self._save_or_get_stock(ticker=ticker, figi=figi)
            if old_levels.get("RSI"):
                with self.db.atomic():
                    query = old_levels.copy()
                    query["from_stock"], query["datetime"] = stock, datetime.now()
                    Indicator.insert_many(query).execute()
                    logger.info("Old prices saved successfully.")
        except Exception as e:
            logger.exception(f"Exception in save old prices (indicators) method: \n{e}\n")
        finally:
            self.db.close()

    def load_old_prices(self, ticker: str, figi: str):
        try:
            stock, create = self._save_or_get_stock(ticker=ticker, figi=figi)
            if not create:
                self.db.connect()
                last_query = Indicator.select().where(Indicator.from_stock == stock).order_by(Indicator.datetime.desc()).dicts().first()
                logger.info("Old prices loaded successfully.")
                return last_query
        except Exception as e:
            logger.exception(f"Exception in load old prices (indicators) method: \n{e}\n")
        finally:
            self.db.close()


database_connector = DatabaseConnector(database)
