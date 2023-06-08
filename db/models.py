from peewee import *

from config_data.config import load_config


config = load_config()

database = PostgresqlDatabase(database=config.db.database,
                              host=config.db.db_host,
                              user=config.db.db_user,
                              password=config.db.db_password)


class BaseModel(Model):
    class Meta:
        database = database


class Stock(BaseModel):
    stock_id = AutoField()
    ticker = CharField(max_length=50, unique=True, null=False)
    figi = CharField(max_length=150, unique=True, null=False)

    class Meta:
        db_table = "stock"


class Indicator(BaseModel):
    indicator_id = AutoField()
    from_stock = ForeignKeyField(Stock, backref='indicators', on_delete="cascade", on_update='cascade')
    datetime = DateTimeField(null=False)
    PRICE = FloatField(null=False)
    MA20 = FloatField(null=False)
    MA50 = FloatField(null=False)
    MA100 = FloatField(null=False)
    MA200 = FloatField(null=False)
    YESTERDAY_LOW = FloatField(null=False)
    YESTERDAY_HIGH = FloatField(null=False)
    WEEK_LOW = FloatField(null=False)
    WEEK_HIGH = FloatField(null=False)
    MONTH_LOW = FloatField(null=False)
    MONTH_HIGH = FloatField(null=False)
    RSI = FloatField(null=False)
    MACD = FloatField(null=False)
    MACDs = FloatField(null=False)
    MA20_HOUR = FloatField(null=False)
    MA50_HOUR = FloatField(null=False)

    class Meta:
        db_table = "indicator"
