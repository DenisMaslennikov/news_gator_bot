"""add_news_sent_model

Revision ID: 0005
Revises: 0004
Create Date: 2024-08-22 17:36:36.871060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0005'
down_revision: Union[str, None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bot_news_sent',
    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Идентификатор'),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('news_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['news_id'], ['nf_news.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['bot_users.user_id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Информация об отправленных новостях.'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bot_news_sent')
    # ### end Alembic commands ###