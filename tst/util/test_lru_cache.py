import unittest

from util.lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_get_put(self):
        cache = LRUCache(2)
        cache.put(1, 'one')
        cache.put(2, 'two')
        self.assertEqual(cache.get(1), 'one')
        self.assertEqual(cache.get(2), 'two')

    def test_eviction(self):
        cache = LRUCache(2)
        cache.put(1, 'one')
        cache.put(2, 'two')
        cache.put(3, 'three')
        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), 'two')
        self.assertEqual(cache.get(3), 'three')

    def test_update(self):
        cache = LRUCache(2)
        cache.put(1, 'one')
        cache.put(2, 'two')
        cache.put(1, 'ONE')
        self.assertEqual(cache.get(1), 'ONE')
        self.assertEqual(cache.get(2), 'two')

    def test_order(self):
        cache = LRUCache(2)
        cache.put(1, 'one')
        cache.put(2, 'two')
        cache.get(1)
        cache.put(3, 'three')
        self.assertEqual(cache.get(1), 'one')
        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(3), 'three')

    def test_capacity(self):
        cache = LRUCache(3)
        cache.put(1, 'one')
        cache.put(2, 'two')
        cache.put(3, 'three')
        cache.put(4, 'four')
        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), 'two')
        self.assertEqual(cache.get(3), 'three')
        self.assertEqual(cache.get(4), 'four')
