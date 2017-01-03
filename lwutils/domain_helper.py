from IPy import IP
import tldextract


def extract_domain(host):
    try:
        d = tldextract.extract(host.encode('utf-8'))
        if d.domain and d.tld:
            return "{}.{}".format(d.domain, d.tld)
        elif d.tld:
            return "{}".format(d.tld)
        elif d.domain and IP(host.split(':')[0]):
            return "{}".format(d.domain)
    except Exception:
        pass
    return ""


def strip_website_hostname(message):
    if "httpHost" in message:
        domain = extract_domain(message['httpHost'])
        if domain:
            message["httpHost"] = domain
