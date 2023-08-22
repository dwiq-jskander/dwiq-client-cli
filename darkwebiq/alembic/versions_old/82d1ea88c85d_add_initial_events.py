"""Add initial event tables

Revision ID: 82d1ea88c85d
Revises: 987fb490001f
Create Date: 2023-08-07 15:09:40.968163

"""
import time

from alembic import op

# revision identifiers, used by Alembic.
revision = "82d1ea88c85d"
down_revision = "987fb490001f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    time.sleep(2)
    op.execute(
        """
CREATE TABLE
zip_files_events (
    id STRING(64) NOT NULL,
    file_name STRING(128) NOT NULL,
    md5_hash STRING(32) NOT NULL,
    bucket STRING(128),
    path STRING(1024) NOT NULL,
    created_at DATETIME NOT NULL,
)
PARTITION BY
  DATETIME_TRUNC(created_at, DAY);
"""
    )
    op.execute(
        """
CREATE TABLE
zip_files_runs_errors_events (
    id STRING(64) NOT NULL,
    zip_file_run_id STRING(64) NOT NULL,
    path STRING(1024),
    error STRING(2048),
    created_at DATETIME NOT NULL,
)
PARTITION BY
  DATETIME_TRUNC(created_at, DAY);
ALTER TABLE zip_files_runs_errors ADD CONSTRAINT fk_zip_files_runs_errors_zip_files_runs FOREIGN KEY (zip_file_run_id)
    REFERENCES zip_files_runs(id) NOT ENFORCED;
"""  # noqa
    )
    op.execute(
        """
CREATE TABLE
zip_files_runs_events (
    id STRING(64) NOT NULL,
    zip_file_id STRING(64) NOT NULL,
    has_errors BOOLEAN NOT NULL,
    is_duplicate BOOLEAN NOT NULL,
    status STRING(12) NOT NULL,
    bucket STRING(128),
    path STRING(1024) NOT NULL,
    file_name STRING(128),
    created_at DATETIME NOT NULL,
)
PARTITION BY
  DATETIME_TRUNC(created_at, DAY);
ALTER TABLE zip_files_runs ADD CONSTRAINT fk_zip_files_runs_zip_files FOREIGN KEY (zip_file_id)
    REFERENCES zip_files(id) NOT ENFORCED;
"""  # noqa
    )

    op.execute(
        """
CREATE TABLE
bots_events (
    id STRING(64) NOT NULL,
    zip_file_id STRING(64) NOT NULL,
    path STRING(1024) NOT NULL,
    uid STRING(128),
    country_code STRING(2),
    ip_address STRING(24),
    date_time DATETIME,
    created_at DATETIME NOT NULL
)
PARTITION BY
  DATETIME_TRUNC(created_at, DAY);
ALTER TABLE bots ADD CONSTRAINT fk_bots_zip_files FOREIGN KEY (zip_file_id)
    REFERENCES zip_files(id) NOT ENFORCED;
"""
    )
    op.execute(
        """
CREATE TABLE
files_events (
    id STRING(64) NOT NULL,
    zip_file_id STRING(64) NOT NULL,
    bot_id STRING(64) NOT NULL,
    path STRING(1024) NOT NULL,
    created_at DATETIME NOT NUL,
)
PARTITION BY
  DATETIME_TRUNC(created_at, DAY);
ALTER TABLE files ADD PRIMARY KEY (id) NOT ENFORCED;
ALTER TABLE files ADD CONSTRAINT fk_files_zip_files FOREIGN KEY (zip_file_id)
    REFERENCES zip_files(id) NOT ENFORCED;
ALTER TABLE files ADD CONSTRAINT fk_files_bots FOREIGN KEY (bot_id)
    REFERENCES bots(id) NOT ENFORCED;
"""
    )
    op.execute(
        """
CREATE TABLE
system_infos_events (
    id STRING(64) NOT NULL,
    zip_file_id STRING(64) NOT NULL,
    file_id STRING(64) NOT NULL,
    ip_address STRING(24),
    exec_path STRING(512),
    build_id STRING(128),
    user STRING(512),
    hwid STRING(256),
    os STRING(256),
    date_time DATETIME,
    country_code STRING(2),
    created_at DATETIME NOT NULL
)
PARTITION BY
  DATETIME_TRUNC(created_at, DAY);
ALTER TABLE system_infos ADD CONSTRAINT fk_system_infos_zip_files FOREIGN KEY (zip_file_id)
    REFERENCES zip_files(id) NOT ENFORCED;
ALTER TABLE system_infos ADD CONSTRAINT fk_sytem_infos_files FOREIGN KEY (file_id)
    REFERENCES files(id) NOT ENFORCED;
"""  # noqa
    )

    op.execute(
        """
CREATE TABLE
passwords_events (
    id STRING(64) NOT NULL,
    zip_file_id STRING(64) NOT NULL,
    file_id STRING(64) NOT NULL,
    url STRING(2056),
    username STRING(512),
    is_user_email BOOLEAN NOT NULL,
    has_password BOOLEAN NOT NULL,
    application STRING(256),
    created_at DATETIME NOT NULL
)
PARTITION BY
  DATETIME_TRUNC(created_at, DAY);
ALTER TABLE passwords ADD CONSTRAINT fk_passwords_zip_files FOREIGN KEY (zip_file_id)
    REFERENCES zip_files(id) NOT ENFORCED;
ALTER TABLE passwords ADD CONSTRAINT fk_passwords_files FOREIGN KEY (file_id)
    REFERENCES files(id) NOT ENFORCED;
"""
    )


def downgrade() -> None:
    op.drop_table("zip_files_events")
    op.drop_table("zip_files_runs_events")
    op.drop_table("zip_files_runs_errors_events")
    op.drop_table("bots_events")
    op.drop_table("files_events")
    op.drop_table("system_info_events")
    op.drop_table("passwords_events")
