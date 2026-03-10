# mkpipe-extractor-mysql

MySQL extractor plugin for [MkPipe](https://github.com/mkpipe-etl/mkpipe). Reads MySQL tables via JDBC.

## Documentation

For more detailed documentation, please visit the [GitHub repository](https://github.com/mkpipe-etl/mkpipe).

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

## Connection Configuration

```yaml
connections:
  mysql_source:
    variant: mysql
    host: localhost
    port: 3306
    database: mydb
    user: myuser
    password: mypassword
```

---

## Table Configuration

```yaml
pipelines:
  - name: mysql_to_pg
    source: mysql_source
    destination: pg_target
    tables:
      - name: orders
        target_name: stg_orders
        replication_method: full
        fetchsize: 100000
```

### Incremental Replication

```yaml
      - name: orders
        target_name: stg_orders
        replication_method: incremental
        iterate_column: updated_at
        iterate_column_type: datetime
        partitions_column: id
        partitions_count: 4
        fetchsize: 50000
```

### Custom SQL

```yaml
      - name: orders
        target_name: stg_orders
        replication_method: incremental
        iterate_column: updated_at
        iterate_column_type: datetime
        custom_query: "SELECT id, user_id, total FROM orders WHERE {query_filter}"
```

---

## Read Parallelism

Set `partitions_column` and `partitions_count` to read in parallel via multiple JDBC connections:

```yaml
      - name: events
        target_name: stg_events
        replication_method: incremental
        iterate_column: created_at
        iterate_column_type: datetime
        partitions_column: id
        partitions_count: 8
        fetchsize: 50000
```

### Performance Notes

- `partitions_column` should be a numeric column (e.g. primary key).
- MySQL JDBC streaming requires `fetchsize: Integer.MIN_VALUE` to avoid loading all rows into memory — mkpipe uses a positive `fetchsize` which works with standard cursors. For very large tables, keep `fetchsize` moderate (50,000–100,000).
- Partitioning only applies to incremental replication.

---

## All Table Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | string | required | MySQL table name |
| `target_name` | string | required | Destination table name |
| `replication_method` | `full` / `incremental` | `full` | Replication strategy |
| `iterate_column` | string | — | Column used for incremental watermark |
| `iterate_column_type` | `int` / `datetime` | — | Type of `iterate_column` |
| `partitions_column` | string | same as `iterate_column` | Column to split JDBC reads on |
| `partitions_count` | int | `10` | Number of parallel JDBC partitions |
| `fetchsize` | int | `100000` | Rows per JDBC fetch |
| `custom_query` | string | — | Override SQL with `{query_filter}` placeholder |
| `custom_query_file` | string | — | Path to SQL file (relative to `sql/` dir) |
| `tags` | list | `[]` | Tags for selective pipeline execution |
| `pass_on_error` | bool | `false` | Skip table on error instead of failing |