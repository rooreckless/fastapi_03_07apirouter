FROM postgres:17.5-bullseye

# 本番環境用PostgreSQL設定
# パフォーマンスとセキュリティの最適化

# 本番用PostgreSQL設定ファイルを追加
RUN echo "# 本番環境用PostgreSQL設定" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "max_connections = 200" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "shared_buffers = 256MB" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "effective_cache_size = 1GB" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "work_mem = 4MB" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "maintenance_work_mem = 64MB" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "checkpoint_completion_target = 0.9" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "wal_buffers = 16MB" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "default_statistics_target = 100" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "log_destination = 'stderr'" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "log_checkpoints = on" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "log_connections = on" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "log_disconnections = on" >> /usr/share/postgresql/postgresql.conf.sample

# セキュリティ強化
RUN echo "ssl = off" >> /usr/share/postgresql/postgresql.conf.sample
