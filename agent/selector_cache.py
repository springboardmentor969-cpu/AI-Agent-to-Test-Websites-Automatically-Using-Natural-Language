# agent/selector_cache.py

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict

class SelectorCache:
    """
    Cache for successful selector healings to improve performance
    and reduce API calls to Grok.
    """
    
    def __init__(self, cache_file: str = "tests/selector_cache.json", ttl_days: int = 30):
        self.cache_file = cache_file
        self.ttl_days = ttl_days
        self.cache: Dict = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Cache load error: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Cache save error: {e}")
    
    def _generate_key(self, url: str, failed_selector: str, action_hint: str) -> str:
        """Generate unique cache key"""
        # Use domain instead of full URL for better cache hits
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        key_string = f"{domain}:{failed_selector}:{action_hint}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, url: str, failed_selector: str, action_hint: str) -> Optional[str]:
        """Get cached selector if available and not expired"""
        key = self._generate_key(url, failed_selector, action_hint)
        
        if key in self.cache:
            entry = self.cache[key]
            cached_time = datetime.fromisoformat(entry['timestamp'])
            
            # Check if cache entry is still valid
            if datetime.now() - cached_time < timedelta(days=self.ttl_days):
                entry['hits'] = entry.get('hits', 0) + 1
                self._save_cache()
                return entry['healed_selector']
            else:
                # Remove expired entry
                del self.cache[key]
                self._save_cache()
        
        return None
    
    def set(self, url: str, failed_selector: str, action_hint: str, healed_selector: str, method: str = "AI"):
        """Store successful healing in cache"""
        key = self._generate_key(url, failed_selector, action_hint)
        
        self.cache[key] = {
            'failed_selector': failed_selector,
            'healed_selector': healed_selector,
            'action_hint': action_hint,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'hits': 0,
            'url_pattern': urlparse(url).netloc if url else 'unknown'
        }
        
        self._save_cache()
    
    def clear_expired(self):
        """Remove all expired cache entries"""
        current_time = datetime.now()
        expired_keys = []
        
        for key, entry in self.cache.items():
            cached_time = datetime.fromisoformat(entry['timestamp'])
            if current_time - cached_time >= timedelta(days=self.ttl_days):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()
            print(f"Cleared {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_entries = len(self.cache)
        total_hits = sum(entry.get('hits', 0) for entry in self.cache.values())
        
        methods = {}
        for entry in self.cache.values():
            method = entry.get('method', 'unknown')
            methods[method] = methods.get(method, 0) + 1
        
        return {
            'total_entries': total_entries,
            'total_hits': total_hits,
            'methods': methods,
            'cache_file': self.cache_file
        }
    
    def clear_all(self):
        """Clear entire cache"""
        self.cache = {}
        self._save_cache()
        print("Cache cleared")


# Import urlparse at module level
from urllib.parse import urlparse
