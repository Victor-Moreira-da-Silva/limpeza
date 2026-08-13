from alembic import op
import sqlalchemy as sa
revision='0001_initial_schema'; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
    from app.db.session import Base
    from app import models
    bind=op.get_bind(); Base.metadata.create_all(bind)
def downgrade():
    from app.db.session import Base
    bind=op.get_bind(); Base.metadata.drop_all(bind)
