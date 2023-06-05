from peewee import *
from config_data.config import load_config

config = load_config()

db = PostgresqlDatabase(database=config.db.database,
                        host=config.db.db_host,
                        user=config.db.db_user,
                        password=config.db.db_password)


class BaseModel(Model):
    class Meta:
        database = db


class Stock(BaseModel):
    stock_id = AutoField()
    ticker = CharField(max_length=50, unique=True, null=False)
    figi = CharField(max_length=150, unique=True, null=False)

    class Meta:
        db_table = "stock"


class Indicator(BaseModel):
    indicator_id = AutoField()
    from_stock = ForeignKeyField(Stock, backref='indicators', on_delete="cascade", on_update='cascade')
    price = FloatField(null=False)
    ma20 = FloatField(null=False)
    ma50 = FloatField(null=False)
    ma100 = FloatField(null=False)
    ma200 = FloatField(null=False)
    yesterday_low = FloatField(null=False)
    yesterday_high = FloatField(null=False)
    week_low = FloatField(null=False)
    week_high = FloatField(null=False)
    month_low = FloatField(null=False)
    month_high = FloatField(null=False)
    rsi = FloatField(null=False)
    macd = FloatField(null=False)
    macds = FloatField(null=False)
    ma20_hour = FloatField(null=False)
    ma50_hour = FloatField(null=False)
    date = DateTimeField(null=False)

    class Meta:
        db_table = "indicator"
