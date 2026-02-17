"""
API rate limiting with exponential backoff.

This module provides client-side rate limiting to prevent exceeding
Gmail API quotas and handle rate limit errors gracefully.
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Callable, Any
from functools import wraps
import logging


logger = logging.getLogger(__name__)


class RateLimitError(Exception):
    """Raised when rate limit is exceeded and retries exhausted."""
    pass


class RateLimiter:
    """Handles API rate limiting with exponential backoff."""
    
    def __init__(
        self,
        requests_per_second: float = 10.0,
        max_retries: int = 5,
        initial_backoff: float = 1.0,
        max_backoff: float = 60.0,
        backoff_multiplier: float = 2.0
    ):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second
            max_retries: Maximum number of retry attempts
            initial_backoff: Initial backoff time in seconds
            max_backoff: Maximum backoff time in seconds
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second if requests_per_second > 0 else 0
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff
        self.backoff_multiplier = backoff_multiplier
        
        # Track last request time per endpoint
        self._last_request_times: Dict[str, float] = {}
        
        # Track rate limit status
        self._rate_limited_until: Dict[str, datetime] = {}
    
    def wait_if_needed(self, endpoint: str = "default"):
        """
        Wait if necessary to respect rate limit.
        
        Args:
            endpoint: API endpoint identifier
        """
        if self.min_interval == 0:
            return  # Rate limiting disabled
        
        # Check if we're currently rate limited
        if endpoint in self._rate_limited_until:
            wait_until = self._rate_limited_until[endpoint]
            if datetime.now() < wait_until:
                wait_seconds = (wait_until - datetime.now()).total_seconds()
                logger.info(f"Rate limited on {endpoint}, waiting {wait_seconds:.2f}s")
                time.sleep(wait_seconds)
            else:
                # Rate limit period expired
                del self._rate_limited_until[endpoint]
        
        # Throttle based on requests per second
        last_request = self._last_request_times.get(endpoint, 0)
        elapsed = time.time() - last_request
        
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            time.sleep(wait_time)
        
        self._last_request_times[endpoint] = time.time()
    
    def calculate_backoff(self, retry_count: int, jitter: bool = True) -> float:
        """
        Calculate exponential backoff time.
        
        Args:
            retry_count: Current retry attempt (0-indexed)
            jitter: Whether to add random jitter
            
        Returns:
            float: Backoff time in seconds
        """
        backoff = min(
            self.initial_backoff * (self.backoff_multiplier ** retry_count),
            self.max_backoff
        )
        
        # Add jitter (±10%) to prevent thundering herd
        if jitter:
            import random
            jitter_factor = random.uniform(0.9, 1.1)
            backoff *= jitter_factor
        
        return backoff
    
    def handle_rate_limit_error(
        self,
        endpoint: str,
        retry_after: Optional[int] = None
    ):
        """
        Handle rate limit error from API.
        
        Args:
            endpoint: API endpoint that was rate limited
            retry_after: Seconds to wait before retry (from API response)
        """
        if retry_after:
            wait_until = datetime.now() + timedelta(seconds=retry_after)
        else:
            # Default to 60 seconds if not specified
            wait_until = datetime.now() + timedelta(seconds=60)
        
        self._rate_limited_until[endpoint] = wait_until
        logger.warning(
            f"Rate limit hit on {endpoint}, "
            f"waiting until {wait_until.strftime('%H:%M:%S')}"
        )
    
    def is_rate_limited(self, endpoint: str = "default") -> bool:
        """
        Check if endpoint is currently rate limited.
        
        Args:
            endpoint: API endpoint to check
            
        Returns:
            bool: True if rate limited
        """
        if endpoint not in self._rate_limited_until:
            return False
        
        if datetime.now() >= self._rate_limited_until[endpoint]:
            del self._rate_limited_until[endpoint]
            return False
        
        return True
    
    def get_rate_limit_status(self, endpoint: str = "default") -> Dict[str, Any]:
        """
        Get rate limit status for endpoint.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            Dict with status information
        """
        status = {
            'endpoint': endpoint,
            'rate_limited': self.is_rate_limited(endpoint),
            'requests_per_second': self.requests_per_second,
        }
        
        if endpoint in self._rate_limited_until:
            wait_until = self._rate_limited_until[endpoint]
            status['rate_limited_until'] = wait_until.isoformat()
            status['seconds_remaining'] = (wait_until - datetime.now()).total_seconds()
        
        return status


def with_retry(
    rate_limiter: Optional[RateLimiter] = None,
    endpoint: str = "default",
    max_retries: Optional[int] = None,
    retryable_exceptions: tuple = (Exception,)
):
    """
    Decorator to add retry logic with exponential backoff.
    
    Args:
        rate_limiter: RateLimiter instance to use
        endpoint: API endpoint identifier
        max_retries: Maximum retry attempts (overrides rate_limiter setting)
        retryable_exceptions: Tuple of exceptions to retry on
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter = rate_limiter or RateLimiter()
            retries = max_retries if max_retries is not None else limiter.max_retries
            
            last_exception = None
            
            for attempt in range(retries + 1):
                try:
                    # Wait if needed before request
                    limiter.wait_if_needed(endpoint)
                    
                    # Execute function
                    result = func(*args, **kwargs)
                    
                    # Success - log recovery if we had failures
                    if attempt > 0:
                        logger.info(
                            f"Request succeeded on attempt {attempt + 1} "
                            f"for {endpoint}"
                        )
                    
                    return result
                    
                except retryable_exceptions as e:
                    last_exception = e
                    
                    # Check if this is a rate limit error
                    is_rate_limit = (
                        hasattr(e, 'resp') and 
                        hasattr(e.resp, 'status') and 
                        e.resp.status == 429
                    )
                    
                    if is_rate_limit:
                        # Extract retry-after header if available
                        retry_after = None
                        if hasattr(e.resp, 'get'):
                            retry_after = e.resp.get('retry-after')
                            if retry_after:
                                try:
                                    retry_after = int(retry_after)
                                except (ValueError, TypeError):
                                    retry_after = None
                        
                        limiter.handle_rate_limit_error(endpoint, retry_after)
                    
                    # Last attempt - raise exception
                    if attempt >= retries:
                        logger.error(
                            f"Request failed after {retries + 1} attempts "
                            f"for {endpoint}: {str(e)}"
                        )
                        raise RateLimitError(
                            f"Max retries ({retries}) exceeded for {endpoint}"
                        ) from e
                    
                    # Calculate backoff and wait
                    backoff = limiter.calculate_backoff(attempt)
                    logger.warning(
                        f"Request failed (attempt {attempt + 1}/{retries + 1}) "
                        f"for {endpoint}, retrying in {backoff:.2f}s: {str(e)}"
                    )
                    time.sleep(backoff)
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
            
        return wrapper
    return decorator


class CachedValue:
    """Simple cache with TTL for reducing API calls."""
    
    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cached value.
        
        Args:
            ttl_seconds: Time to live in seconds
        """
        self.ttl_seconds = ttl_seconds
        self._value: Optional[Any] = None
        self._expires_at: Optional[datetime] = None
    
    def get(self) -> Optional[Any]:
        """
        Get cached value if not expired.
        
        Returns:
            Cached value or None if expired/not set
        """
        if self._value is None or self._expires_at is None:
            return None
        
        if datetime.now() >= self._expires_at:
            self._value = None
            self._expires_at = None
            return None
        
        return self._value
    
    def set(self, value: Any):
        """
        Set cached value with TTL.
        
        Args:
            value: Value to cache
        """
        self._value = value
        self._expires_at = datetime.now() + timedelta(seconds=self.ttl_seconds)
    
    def clear(self):
        """Clear cached value."""
        self._value = None
        self._expires_at = None
    
    def is_valid(self) -> bool:
        """
        Check if cache is valid.
        
        Returns:
            bool: True if cache is valid
        """
        return self.get() is not None


class LabelCache:
    """Cache for Gmail labels to reduce API calls."""
    
    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize label cache.
        
        Args:
            ttl_seconds: Time to live in seconds (default 1 hour)
        """
        self._cache = CachedValue(ttl_seconds)
    
    def get_labels(self) -> Optional[list]:
        """
        Get cached labels.
        
        Returns:
            List of labels or None if cache expired
        """
        return self._cache.get()
    
    def set_labels(self, labels: list):
        """
        Cache labels.
        
        Args:
            labels: List of label objects
        """
        self._cache.set(labels)
    
    def clear(self):
        """Clear label cache."""
        self._cache.clear()
    
    def is_valid(self) -> bool:
        """
        Check if cache is valid.
        
        Returns:
            bool: True if cache is valid
        """
        return self._cache.is_valid()


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None
_label_cache: Optional[LabelCache] = None


def get_rate_limiter(
    enabled: bool = True,
    **kwargs
) -> Optional[RateLimiter]:
    """
    Get global rate limiter instance.
    
    Args:
        enabled: Whether rate limiting is enabled
        **kwargs: Arguments to pass to RateLimiter constructor
        
    Returns:
        RateLimiter instance or None if disabled
    """
    global _rate_limiter
    
    if not enabled:
        return None
    
    if _rate_limiter is None:
        _rate_limiter = RateLimiter(**kwargs)
    
    return _rate_limiter


def get_label_cache(ttl_seconds: int = 3600) -> LabelCache:
    """
    Get global label cache instance.
    
    Args:
        ttl_seconds: Cache TTL in seconds
        
    Returns:
        LabelCache instance
    """
    global _label_cache
    
    if _label_cache is None:
        _label_cache = LabelCache(ttl_seconds)
    
    return _label_cache


def configure_rate_limiting(
    enabled: bool = True,
    **kwargs
) -> Optional[RateLimiter]:
    """
    Configure global rate limiting.
    
    Args:
        enabled: Whether to enable rate limiting
        **kwargs: Arguments to pass to RateLimiter constructor
        
    Returns:
        Configured RateLimiter instance or None
    """
    global _rate_limiter
    
    if enabled:
        _rate_limiter = RateLimiter(**kwargs)
    else:
        _rate_limiter = None
    
    return _rate_limiter
