import phonenumbers
from urllib.parse import urlparse, parse_qs, unquote

SOCIAL_DOMAINS = [
    "www.instagram.com",
    "www.facebook.com",
    "m.facebook.com",
    "www.tiktok.com",
    "wa.me",
    "x.com",
    "twitter.com",
]


def clean_number(number):
    try:
        parsed = phonenumbers.parse(str(number), "ZA")

        if phonenumbers.is_valid_number(parsed) and parsed.country_code == 27:
            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.NATIONAL
            )

    except Exception:
        pass

    return None


def unwrap_url(url):
    if url and url.startswith("/url?"):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)

        if "q" in qs:
            return unquote(qs["q"][0])

    return url


def get_root_domain(url):
    if not url:
        return None

    parsed = urlparse(url)

    if not parsed.netloc:
        return None

    if parsed.netloc in SOCIAL_DOMAINS:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    return f"{parsed.scheme}://{parsed.netloc}"


def clean_url(url):
    if not url:
        return None

    return get_root_domain(unwrap_url(url))