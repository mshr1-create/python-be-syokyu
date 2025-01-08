# ベースイメージ
FROM mysql:8

# 必要な設定やファイルのコピー
# 例: ログディレクトリの作成と権限変更
RUN mkdir -p /var/log/mysql && chown mysql:mysql /var/log/mysql

# その他の設定
ENV MYSQL_ROOT_PASSWORD=yourpassword
ENV MYSQL_DATABASE=yourdatabase

# ポートの公開
EXPOSE 3306
