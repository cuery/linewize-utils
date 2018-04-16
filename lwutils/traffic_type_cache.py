import requests
import json
import time


class TrafficTypeCache(object):
    def __init__(self, appindex_url, expiry=7200, keep_criteria=False):
        self.appindex_url = appindex_url
        self.expiry = expiry
        self.last_update = None
        self.signature_cache = {}
        self.fingerprint_cache = {}
        self.keep_criteria = keep_criteria

    def _cache_expired(self):
        return self.last_update is None or (time.time() - self.last_update) > self.expiry

    def __get_appindex_signature_uri(self):
        response = requests.get(self.get_app_index_url())
        return json.loads(response.text)["signatures"]

    def __get_appindex_fingerprints_uri(self):
        response = requests.get(self.get_app_index_url())
        return json.loads(response.text)["fingerprints"]

    def get_appindex_keywords(self, key):
        response = requests.get(self.get_app_index_url() + "/keywords/category/" + key)
        return json.loads(response.text)["category"]

    def get_appindex_keyword_categories(self):
        response = requests.get(self.get_app_index_url() + "/keywords/categories")
        return json.loads(response.text)["categories"]

    def get_app_index_url(self):
        return self.appindex_url

    def _reload_signature_cache(self):
        response = requests.get(self.__get_appindex_signature_uri())
        appindex = json.loads(response.text)
        tmp_siganture_cache = {}
        if 'signatures' in appindex:
            for signature in appindex['signatures']:
                if not self.keep_criteria:
                    del signature["criteria"]
                tmp_siganture_cache[signature['id']] = signature
            self.signature_cache = tmp_siganture_cache
            self.last_update = time.time()

    def _reload_fingerprint_cache(self):
        response = requests.get(self.__get_appindex_fingerprints_uri())
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

    def get_normalized_signatures(self):
        self._reload_cache()
        ret = []
        for item in self.signature_cache.itervalues():
            ret.append(item)
        return ret

    def get_all_fingerprints(self):
        self._reload_cache()
        return self.fingerprint_cache

    def get_normalized_fingerprints(self):
        self._reload_cache()
        ret = []
        for item in self.fingerprint_cache.itervalues():
            ret.append(item)
        return ret

    def get_signature(self, signature_id):
        self._reload_cache()
        direct_hit_sig = self.signature_cache.get(signature_id)
        if direct_hit_sig:
            return direct_hit_sig
        return self.get_signature_by_name(signature_id)

    def get_signature_children(self, signature_id):
        self._reload_cache()
        ret = []
        for signature in self.signature_cache.values():
            if signature.get("category") == signature_id:
                ret.append(signature)
        return ret

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
            print "Failed to load signatures form " + self.get_app_index_url()
            print e
            return signature_id
