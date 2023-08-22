"""Initial table creation in BigQuery

Revision ID: 98e7e55ff987
Revises:
Create Date: 2023-08-22 17:32:20.361167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '98e7e55ff987'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create the BigQuery table
    op.execute(
        """
CREATE TABLE IF NOT EXISTS `all_client_list` (
    company STRING,
    url STRING,
    source STRING,
    notification STRING,
    intervention STRING,
    group_reference STRING,
    policy_reference STRING
)
"""
    )

def downgrade() -> None:
    # Drop the BigQuery table
    op.drop_table("all_client_list")