from alembic import op
import sqlalchemy as sa
revision = "0001_inventory"
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    op.create_table("assets",sa.Column("id",sa.Integer(),primary_key=True),
      sa.Column("asset_tag",sa.String(40),nullable=False,unique=True),sa.Column("name",sa.String(160),nullable=False),
      sa.Column("category",sa.String(50),nullable=False),sa.Column("description",sa.Text(),nullable=False),
      sa.Column("total",sa.Integer(),nullable=False),sa.Column("available",sa.Integer(),nullable=False),
      sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),
      sa.CheckConstraint("available >= 0 AND available <= total",name="valid_stock"))
    op.create_table("loans",sa.Column("id",sa.Integer(),primary_key=True),
      sa.Column("asset_id",sa.Integer(),sa.ForeignKey("assets.id"),nullable=False),
      sa.Column("asset_name",sa.String(160),nullable=False),sa.Column("borrower",sa.String(100),nullable=False),
      sa.Column("quantity",sa.Integer(),nullable=False),sa.Column("borrowed_at",sa.DateTime(timezone=True),nullable=False),
      sa.Column("returned_at",sa.DateTime(timezone=True)))
    op.create_index("ix_loans_asset_id","loans",["asset_id"])
def downgrade():
    op.drop_table("loans"); op.drop_table("assets")
