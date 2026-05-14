"""
Shared cooldown for Jira API rate-limit handling.

A small Redis-backed key stores the epoch-second at which it's safe to retry
Jira calls. Any worker (sync or async) that observes a 429 arms the cooldown;
all workers respect it before calling Jira again. This avoids the cascade
where N workers each independently hit 429 in parallel.

Design choices:
  - Fail open: if Redis is down or misconfigured, cooldown_remaining()
    returns 0 and arm_cooldown() is a no-op. Jira pushes proceed at full
    speed and we get 429 alerts the same as today. We don't crash celery
    tasks because Redis hiccupped.
  - Single key, TTL'd. No need for atomic compare-and-set; last-writer-wins
    on the cooldown timestamp is fine — a higher value just means we wait
    longer, which is the safe direction.
  - Lazy connection. The redis client is built on first use so importing
    this module from a context without Redis configured (tests, shell)
    doesn't blow up.
"""
import logging
import random
import time

from django.conf import settings

logger = logging.getLogger(__name__)

COOLDOWN_KEY = 'jira:cooldown_until_epoch'
JITTER_RATIO = 3  # countdown += rand(0, base / JITTER_RATIO) — up to ~33% jitter

_redis_client = None
_redis_init_failed = False


def _get_redis():
    """Return a redis client, or None if not configured / unavailable."""
    global _redis_client, _redis_init_failed
    if _redis_client is not None:
        return _redis_client
    if _redis_init_failed:
        return None
    url = getattr(settings, 'JIRA_RATE_LIMIT_REDIS_URL', '')
    if not url:
        _redis_init_failed = True
        return None
    try:
        import redis
        _redis_client = redis.from_url(url, socket_timeout=2, socket_connect_timeout=2)
        return _redis_client
    except Exception:
        logger.exception('jira rate_limit: failed to initialize redis client; disabling cooldown')
        _redis_init_failed = True
        return None


def cooldown_remaining():
    """Seconds remaining on the active Jira cooldown, or 0 if none/disabled."""
    r = _get_redis()
    if r is None:
        return 0
    try:
        val = r.get(COOLDOWN_KEY)
    except Exception:
        logger.warning('jira rate_limit: redis GET failed; treating as no cooldown', exc_info=True)
        return 0
    if not val:
        return 0
    try:
        until_epoch = int(val)
    except (TypeError, ValueError):
        return 0
    return max(0, until_epoch - int(time.time()))


def arm_cooldown(retry_after_seconds):
    """Mark Jira as rate-limited for the given number of seconds."""
    if retry_after_seconds <= 0:
        return
    r = _get_redis()
    if r is None:
        return
    until_epoch = int(time.time()) + int(retry_after_seconds)
    try:
        # ex=retry_after + small buffer so the key auto-expires shortly after
        # the cooldown ends and won't linger if no one reads it.
        r.set(COOLDOWN_KEY, until_epoch, ex=int(retry_after_seconds) + 10)
    except Exception:
        logger.warning('jira rate_limit: redis SET failed; cooldown not armed', exc_info=True)


def countdown_with_jitter(base_seconds):
    """Return base_seconds plus random jitter (up to base/JITTER_RATIO).

    Spreads simultaneously-failed tasks across a window so they don't all
    retry at the exact same second and stampede Jira.
    """
    base = max(1, int(base_seconds))
    jitter_ceiling = max(5, base // JITTER_RATIO)
    return base + random.randint(0, jitter_ceiling)
