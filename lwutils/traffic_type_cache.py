import requests
import json
import time


class TrafficTypeCache(object):
    def __init__(self, appindex_url, fingerprint_urls, expiry=7200):
        self.appindex_url = appindex_url
        self.fingerprint_urls = fingerprint_urls
        self.expiry = expiry

        self.last_update = None
        self.signature_cache = {}
        self.fingerprint_cache = {}

    def _cache_expired(self):
        return self.last_update is None or (time.time() - self.last_update) > self.expiry

    def _reload_signature_cache(self):
        print "_reload_signature_cache() called"

        response = requests.get(self.appindex_url)
        appindex = json.loads(response.text)
        tmp_siganture_cache = {}
        if 'signatures' in appindex:
            for signature in appindex['signatures']:
                tmp_siganture_cache[signature['id']] = signature
            self.signature_cache = tmp_siganture_cache
            self.last_update = time.time()

    def _reload_fingerprint_cache(self):
        print "_reload_fingerprint_cache() called"
        response = requests.get(self.fingerprint_urls)
        appindex = json.loads(response.text)
        self.fingerprint_cache = {}
        if 'fingerprints' in appindex:
            for signature in appindex['fingerprints']:
                self.fingerprint_cache[signature['id']] = signature
            self.last_update = time.time()

    def _reload_cache(self):
        if self._cache_expired():
            self._reload_signature_cache()
            self._reload_fingerprint_cache()

    def get_all_signatures(self):
        self._reload_cache()
        return self.signature_cache

    def get_signature(self, signature_id):
        self._reload_cache()
        direct_hit_sig = self.signature_cache.get(signature_id)
        if direct_hit_sig:
            return direct_hit_sig
        return self.get_signature_by_name(signature_id)

    def get_signature_by_name(self, signature_id):
        self._reload_cache()
        for signature_key in self.signature_cache:
            signature = self.signature_cache[signature_key]
            if signature["name"] == signature_id:
                return signature

    def get_fingerprint_by_id(self, fingerprint_id):
        self._reload_cache()
        return self.fingerprint_cache.get(fingerprint_id)

    def get_fingerprint_name_by_id(self, fingerprint_id):
        fingerprint = self.get_fingerprint_by_id(fingerprint_id)
        if fingerprint:
            return fingerprint["name"]
        else:
            return "Unknown"

    def get_signature_name_by_id(self, signature_id):
        try:
            signature = self.get_signature(signature_id)
            if signature:
                return signature["name"]
            else:
                return "Unknown"
        except Exception as e:
            print "Failed to load signatures form " + self.appindex_url
            print e
            return signature_id
