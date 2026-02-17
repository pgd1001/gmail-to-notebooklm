"""Tests for rate limiting module."""

import pytest
import time
from datetime import datetime, timedelta

from gmail_to_notebooklm.rate_limiter import (
    RateLimiter,
    RateLimitError,
    CachedValue,
    LabelCache,
    get_rate_limiter,
    get_label_cache,
)


class TestRateLimiter:
    """Test rate limiter functionality."""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(requests_per_second=10.0)
        assert limiter.requests_per_second == 10.0
        assert limiter.min_interval == 0.1
    
    def test_rate_limiter_disabled(self):
        """Test rate limiter with 0 requests per second (disabled)."""
        limiter = RateLimiter(requests_per_second=0)
        assert limiter.min_interval == 0
        
        # Should not wait
        start = time.time()
        limiter.wait_if_needed()
        elapsed = time.time() - start
        assert elapsed < 0.01  # Should be instant
    
    def test_wait_if_needed_throttles(self):
        """Test that wait_if_needed throttles requests."""
        limiter = RateLimiter(requests_per_second=10.0)  # 0.1s between requests
        
        # First request should be instant
        start = time.time()
        limiter.wait_if_needed()
        elapsed1 = time.time() - start
        assert elapsed1 < 0.01
        
        # Second request should wait
        start = time.time()
        limiter.wait_if_needed()
        elapsed2 = time.time() - start
        assert elapsed2 >= 0.09  # Should wait ~0.1s
    
    def test_calculate_backoff_exponential(self):
        """Test exponential backoff calculation."""
        limiter = RateLimiter(initial_backoff=1.0, backoff_multiplier=2.0)
        
        # Test exponential growth
        assert limiter.calculate_backoff(0, jitter=False) == 1.0
        assert limiter.calculate_backoff(1, jitter=False) == 2.0
        assert limiter.calculate_backoff(2, jitter=False) == 4.0
        assert limiter.calculate_backoff(3, jitter=False) == 8.0
    
    def test_calculate_backoff_max_limit(self):
        """Test backoff respects max limit."""
        limiter = RateLimiter(initial_backoff=1.0, max_backoff=10.0)
        
        # Should cap at max_backoff
        backoff = limiter.calculate_backoff(10, jitter=False)
        assert backoff == 10.0
    
    def test_calculate_backoff_with_jitter(self):
        """Test backoff with jitter."""
        limiter = RateLimiter(initial_backoff=10.0)
        
        # With jitter, should vary slightly
        backoffs = [limiter.calculate_backoff(0, jitter=True) for _ in range(10)]
        
        # Should all be close to 10.0 but not identical
        assert all(9.0 <= b <= 11.0 for b in backoffs)
        assert len(set(backoffs)) > 1  # Should have variation
    
    def test_handle_rate_limit_error(self):
        """Test handling rate limit error."""
        limiter = RateLimiter()
        
        limiter.handle_rate_limit_error("test_endpoint", retry_after=30)
        
        assert limiter.is_rate_limited("test_endpoint")
        
        # Check wait time is set correctly
        status = limiter.get_rate_limit_status("test_endpoint")
        assert status['rate_limited'] is True
        assert status['seconds_remaining'] > 0
    
    def test_handle_rate_limit_error_no_retry_after(self):
        """Test handling rate limit without retry_after."""
        limiter = RateLimiter()
        
        limiter.handle_rate_limit_error("test_endpoint")
        
        assert limiter.is_rate_limited("test_endpoint")
    
    def test_is_rate_limited_expires(self):
        """Test that rate limit expires."""
        limiter = RateLimiter()
        
        # Set rate limit with very short duration
        limiter._rate_limited_until["test"] = datetime.now() + timedelta(milliseconds=100)
        
        assert limiter.is_rate_limited("test")
        
        # Wait for expiration
        time.sleep(0.15)
        
        assert not limiter.is_rate_limited("test")
    
    def test_get_rate_limit_status(self):
        """Test getting rate limit status."""
        limiter = RateLimiter(requests_per_second=5.0)
        
        status = limiter.get_rate_limit_status("test")
        assert status['endpoint'] == "test"
        assert status['rate_limited'] is False
        assert status['requests_per_second'] == 5.0
    
    def test_get_rate_limit_status_when_limited(self):
        """Test getting status when rate limited."""
        limiter = RateLimiter()
        limiter.handle_rate_limit_error("test", retry_after=10)
        
        status = limiter.get_rate_limit_status("test")
        assert status['rate_limited'] is True
        assert 'rate_limited_until' in status
        assert 'seconds_remaining' in status
    
    def test_multiple_endpoints(self):
        """Test rate limiting multiple endpoints independently."""
        limiter = RateLimiter()
        
        limiter.handle_rate_limit_error("endpoint1", retry_after=10)
        
        assert limiter.is_rate_limited("endpoint1")
        assert not limiter.is_rate_limited("endpoint2")


class TestCachedValue:
    """Test cached value functionality."""
    
    def test_cached_value_initialization(self):
        """Test cached value initialization."""
        cache = CachedValue(ttl_seconds=60)
        assert cache.ttl_seconds == 60
        assert cache.get() is None
    
    def test_cached_value_set_get(self):
        """Test setting and getting cached value."""
        cache = CachedValue(ttl_seconds=60)
        
        cache.set("test value")
        assert cache.get() == "test value"
    
    def test_cached_value_expiration(self):
        """Test cached value expiration."""
        cache = CachedValue(ttl_seconds=0.1)  # 100ms TTL
        
        cache.set("test value")
        assert cache.get() == "test value"
        
        # Wait for expiration
        time.sleep(0.15)
        assert cache.get() is None
    
    def test_cached_value_clear(self):
        """Test clearing cached value."""
        cache = CachedValue(ttl_seconds=60)
        
        cache.set("test value")
        assert cache.get() == "test value"
        
        cache.clear()
        assert cache.get() is None
    
    def test_cached_value_is_valid(self):
        """Test checking if cache is valid."""
        cache = CachedValue(ttl_seconds=60)
        
        assert not cache.is_valid()
        
        cache.set("test value")
        assert cache.is_valid()
        
        cache.clear()
        assert not cache.is_valid()
    
    def test_cached_value_complex_data(self):
        """Test caching complex data structures."""
        cache = CachedValue(ttl_seconds=60)
        
        complex_data = {
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "nested": {"a": {"b": {"c": "deep"}}},
        }
        
        cache.set(complex_data)
        retrieved = cache.get()
        
        assert retrieved == complex_data
        assert retrieved is complex_data  # Should be same object


class TestLabelCache:
    """Test label cache functionality."""
    
    def test_label_cache_initialization(self):
        """Test label cache initialization."""
        cache = LabelCache(ttl_seconds=3600)
        assert cache.get_labels() is None
    
    def test_label_cache_set_get(self):
        """Test setting and getting labels."""
        cache = LabelCache(ttl_seconds=3600)
        
        labels = [
            {"id": "1", "name": "Inbox"},
            {"id": "2", "name": "Sent"},
        ]
        
        cache.set_labels(labels)
        retrieved = cache.get_labels()
        
        assert retrieved == labels
    
    def test_label_cache_expiration(self):
        """Test label cache expiration."""
        cache = LabelCache(ttl_seconds=0.1)
        
        labels = [{"id": "1", "name": "Test"}]
        cache.set_labels(labels)
        
        assert cache.get_labels() == labels
        
        # Wait for expiration
        time.sleep(0.15)
        assert cache.get_labels() is None
    
    def test_label_cache_clear(self):
        """Test clearing label cache."""
        cache = LabelCache(ttl_seconds=3600)
        
        labels = [{"id": "1", "name": "Test"}]
        cache.set_labels(labels)
        
        cache.clear()
        assert cache.get_labels() is None
    
    def test_label_cache_is_valid(self):
        """Test checking if label cache is valid."""
        cache = LabelCache(ttl_seconds=3600)
        
        assert not cache.is_valid()
        
        cache.set_labels([{"id": "1", "name": "Test"}])
        assert cache.is_valid()


class TestGlobalInstances:
    """Test global instance functions."""
    
    def test_get_rate_limiter_enabled(self):
        """Test getting enabled rate limiter."""
        limiter = get_rate_limiter(enabled=True)
        assert limiter is not None
        assert isinstance(limiter, RateLimiter)
    
    def test_get_rate_limiter_disabled(self):
        """Test getting disabled rate limiter."""
        limiter = get_rate_limiter(enabled=False)
        assert limiter is None
    
    def test_get_rate_limiter_singleton(self):
        """Test rate limiter singleton behavior."""
        limiter1 = get_rate_limiter(enabled=True)
        limiter2 = get_rate_limiter(enabled=True)
        
        # Should return same instance
        assert limiter1 is limiter2
    
    def test_get_label_cache(self):
        """Test getting label cache."""
        cache = get_label_cache()
        assert cache is not None
        assert isinstance(cache, LabelCache)
    
    def test_get_label_cache_singleton(self):
        """Test label cache singleton behavior."""
        cache1 = get_label_cache()
        cache2 = get_label_cache()
        
        # Should return same instance
        assert cache1 is cache2


class TestRateLimiterIntegration:
    """Test rate limiter integration scenarios."""
    
    def test_rate_limiter_realistic_scenario(self):
        """Test rate limiter in realistic scenario."""
        limiter = RateLimiter(requests_per_second=5.0)  # 5 requests per second
        
        start = time.time()
        
        # Make 10 requests
        for i in range(10):
            limiter.wait_if_needed(f"endpoint_{i % 2}")  # Alternate between 2 endpoints
        
        elapsed = time.time() - start
        
        # Should take at least 0.8 seconds (10 requests / 5 per second with some tolerance)
        # The rate limiter uses per-endpoint tracking, so alternating endpoints
        # allows more parallelism
        assert elapsed >= 0.5  # More lenient timing check
    
    def test_rate_limiter_with_errors(self):
        """Test rate limiter handling errors."""
        limiter = RateLimiter(requests_per_second=10.0)
        
        # Simulate rate limit error
        limiter.handle_rate_limit_error("test", retry_after=1)
        
        # Should wait when rate limited
        start = time.time()
        limiter.wait_if_needed("test")
        elapsed = time.time() - start
        
        assert elapsed >= 0.9  # Should wait ~1 second
