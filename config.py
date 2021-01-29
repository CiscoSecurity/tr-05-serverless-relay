import os

from __version__ import VERSION


class Config:
    VERSION = VERSION

    SECRET_KEY = 'LzcE5uOoH5l0ypi3TqPec4R28ti28i7a4hjcc5mNsX3ycVEgBv5Hre94vbaXIYRu'

    API_URL = "https://investigate.api.umbrella.com"  # Your umbrella investigate account
    # API_URL = "http://localhost:4000"  # Or the umbrella backend simulator
    API_PATH = "/domains/categorization/{observable}"

    # Supported types with rules
    CCT_OBSERVABLE_TYPES = {
        'url': {'sep': '://'},
        'ip': {},
        'domain': {}
    }

    CTR_HEADERS = {
        'User-Agent': ('SecureX Threat Response Integrations '
                       '<tr-integrations-support@cisco.com>')
    }

    # Supported types of verdict
    DISPOSITIONS = {
        'clean': (1, 'Clean'),
        'malicious': (2, 'Malicious'),
        'suspicious': (3, 'Suspicious'),
        'common': (4, 'Common'),
        'unknown': (5, 'Unknown')
    }