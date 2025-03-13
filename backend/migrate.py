"""Command-line tool for running database migrations.

Usage:
  python migrate.py upgrade [--revision=<rev>]
  python migrate.py downgrade [--revision=<rev>]
  python migrate.py current
  python migrate.py history
  python migrate.py revision --message=<msg> [--autogenerate]

Examples:
  python migrate.py upgrade                # Upgrade to latest version
  python migrate.py upgrade --revision=123abc  # Upgrade to specific version
  python migrate.py downgrade --revision=-1    # Downgrade one revision
  python migrate.py current                # Show current revision
  python migrate.py history                # Show revision history
  python migrate.py revision --message="Add user table" --autogenerate  # Create a new migration
"""

import os
import sys
import argparse
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command


def get_alembic_config():
    """Get Alembic configuration."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_ini = os.path.join(base_dir, 'alembic.ini')
    
    if not os.path.exists(alembic_ini):
        print(f"Error: Alembic config not found at {alembic_ini}")
        sys.exit(1)
    
    alembic_cfg = AlembicConfig(alembic_ini)
    return alembic_cfg


def main():
    """Run the migration command-line interface."""
    parser = argparse.ArgumentParser(description="Database migration tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Upgrade command
    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade database schema")
    upgrade_parser.add_argument("--revision", default="head", help="Revision to upgrade to")
    
    # Downgrade command
    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade database schema")
    downgrade_parser.add_argument("--revision", required=True, help="Revision to downgrade to")
    
    # Current command
    subparsers.add_parser("current", help="Show current revision")
    
    # History command
    subparsers.add_parser("history", help="Show revision history")
    
    # Revision command
    revision_parser = subparsers.add_parser("revision", help="Create a new migration")
    revision_parser.add_argument("--message", required=True, help="Migration message")
    revision_parser.add_argument("--autogenerate", action="store_true", help="Auto-generate migration based on model changes")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    alembic_cfg = get_alembic_config()
    
    # Run the appropriate command
    if args.command == "upgrade":
        alembic_command.upgrade(alembic_cfg, args.revision)
        print(f"Database upgraded to {args.revision}")
    
    elif args.command == "downgrade":
        alembic_command.downgrade(alembic_cfg, args.revision)
        print(f"Database downgraded to {args.revision}")
    
    elif args.command == "current":
        alembic_command.current(alembic_cfg)
    
    elif args.command == "history":
        alembic_command.history(alembic_cfg)
    
    elif args.command == "revision":
        alembic_command.revision(
            alembic_cfg,
            message=args.message,
            autogenerate=args.autogenerate
        )
        print(f"Created new migration with message: {args.message}")


if __name__ == "__main__":
    main() 