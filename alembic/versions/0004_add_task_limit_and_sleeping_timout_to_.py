"""add_task_limit_and_sleeping_timout_to_resource_model

Revision ID: 0004
Revises: 0003
Create Date: 2024-08-28 14:51:21.220102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0004'
down_revision: Union[str, None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nf_resources', sa.Column('parser_task_limit', sa.SmallInteger(), nullable=True, comment='Максимальное количество одновременных задач парсинга'))
    op.add_column('nf_resources', sa.Column('parser_sleep_timout', sa.SmallInteger(), nullable=True, comment='Интервал времени между задачами парсинга'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nf_resources', 'parser_sleep_timout')
    op.drop_column('nf_resources', 'parser_task_limit')
    # ### end Alembic commands ###