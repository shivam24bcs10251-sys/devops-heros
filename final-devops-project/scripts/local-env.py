"""Generate a local-only database password; never print or replace an existing one."""
from pathlib import Path
import secrets
path=Path(__file__).resolve().parents[1]/'.env'
if not path.exists():
    path.write_text('POSTGRES_PASSWORD='+secrets.token_urlsafe(24)+'\n')
    path.chmod(0o600)
print('Local database environment ready (.env is ignored)')
