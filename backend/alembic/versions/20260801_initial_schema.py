from alembic import op
import sqlalchemy as sa


revision = "20260801_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agencies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_agencies_id"), "agencies", ["id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "properties",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agency_id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=512), nullable=False),
        sa.Column("city", sa.String(length=128), nullable=False),
        sa.Column("postal_code", sa.String(length=20), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("surface", sa.Float(), nullable=True),
        sa.Column("estimated_value", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_properties_id"), "properties", ["id"], unique=False)

    op.create_table(
        "prospects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agency_id", sa.Integer(), nullable=False),
        sa.Column("owner_name", sa.String(length=255), nullable=False),
        sa.Column("property_address", sa.String(length=512), nullable=False),
        sa.Column("city", sa.String(length=128), nullable=False),
        sa.Column("postal_code", sa.String(length=20), nullable=False),
        sa.Column("surface", sa.Float(), nullable=True),
        sa.Column("estimated_value", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_prospects_id"), "prospects", ["id"], unique=False)

    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jobs_id"), "jobs", ["id"], unique=False)

    op.create_table(
        "executions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=True),
        sa.Column("connector", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_executions_id"), "executions", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("executions")
    op.drop_table("jobs")
    op.drop_table("prospects")
    op.drop_table("properties")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("agencies")
