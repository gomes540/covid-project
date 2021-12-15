from google.cloud.bigquery import SchemaField

COVID_RAW_DATA_SCHEMA = [
    SchemaField("date", "DATE"),
    SchemaField("confirmed", "INT64"),
    SchemaField("deaths", "INT64"),
    SchemaField("recovered", "INT64"),
    SchemaField("confirmed_diff", "INT64"),
    SchemaField("deaths_diff", "INT64"),
    SchemaField("recovered_diff", "INT64"),
    SchemaField("last_update", "DATETIME"),
    SchemaField("active", "INT64"),
    SchemaField("active_diff", "INT64"),
    SchemaField("fatality_rate", "FLOAT64"),
    SchemaField("region", "STRING"),
]
