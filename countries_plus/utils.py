# coding=utf-8
import requests

from countries_plus.models import Country

DATA_HEADERS_ORDERED = [
    'ISO', 'ISO3', 'ISO-Numeric', 'fips', 'Country', 'Capital', 'Area(in sq km)',
    'Population', 'Continent', 'tld', 'CurrencyCode', 'CurrencyName', 'Phone',
    'Postal Code Format', 'Postal Code Regex', 'Languages', 'geonameid', 'neighbours',
    'EquivalentFipsCode'
]

DATA_HEADERS_MAP = {
    'ISO': 'iso',
    'ISO3': 'iso3',
    'ISO-Numeric': 'iso_numeric',
    'fips': 'fips',
    'Country': 'name',
    'Capital': 'capital',
    'Area(in sq km)': 'area',
    'Population': 'population',
    'Continent': 'continent',
    'tld': 'tld',
    'CurrencyCode': 'currency_code',
    'CurrencyName': 'currency_name',
    'Phone': 'phone',
    'Postal Code Format': 'postal_code_format',
    'Postal Code Regex': 'postal_code_regex',
    'Languages': 'languages',
    'geonameid': 'geonameid',
    'neighbours': 'neighbours',
    'EquivalentFipsCode': 'equivalent_fips_code'
}

CURRENCY_SYMBOLS = {
    "AED": "د.إ",
    "AFN": "؋",
    "ALL": "L",
    "AMD": "դր.",
    "ANG": "ƒ",
    "AOA": "Kz",
    "ARS": "$",
    "AUD": "$",
    "AWG": "ƒ",
    "AZN": "m",
    "BAM": "KM",
    "BBD": "$",
    "BDT": "৳",
    "BGN": "лв",
    "BHD": "ب.د",
    "BIF": "Fr",
    "BMD": "$",
    "BND": "$",
    "BOB": "Bs.",
    "BRL": "R$",
    "BSD": "$",
    "BTN": "Nu",
    "BWP": "P",
    "BYR": "Br",
    "BZD": "$",
    "CAD": "$",
    "CDF": "Fr",
    "CHF": "Fr",
    "CLP": "$",
    "CNY": "¥",
    "COP": "$",
    "CRC": "₡",
    "CUP": "$",
    "CVE": "$, Esc",
    "CZK": "Kč",
    "DJF": "Fr",
    "DKK": "kr",
    "DOP": "$",
    "DZD": "د.ج",
    "EEK": "KR",
    "EGP": "£,ج.م",
    "ERN": "Nfk",
    "ETB": "Br",
    "EUR": "€",
    "FJD": "$",
    "FKP": "£",
    "GBP": "£",
    "GEL": "ლ",
    "GHS": "₵",
    "GIP": "£",
    "GMD": "D",
    "GNF": "Fr",
    "GTQ": "Q",
    "GYD": "$",
    "HKD": "$",
    "HNL": "L",
    "HRK": "kn",
    "HTG": "G",
    "HUF": "Ft",
    "IDR": "Rp",
    "ILS": "₪",
    "INR": "₨",
    "IQD": "ع.د",
    "IRR": "﷼",
    "ISK": "kr",
    "JMD": "$",
    "JOD": "د.ا",
    "JPY": "¥",
    "KES": "Sh",
    "KGS": "лв",
    "KHR": "៛",
    "KMF": "Fr",
    "KPW": "₩",
    "KRW": "₩",
    "KWD": "د.ك",
    "KYD": "$",
    "KZT": "Т",
    "LAK": "₭",
    "LBP": "ل.ل",
    "LKR": "ரூ",
    "LRD": "$",
    "LSL": "L",
    "LTL": "Lt",
    "LVL": "Ls",
    "LYD": "ل.د",
    "MAD": "د.م.",
    "MDL": "L",
    "MGA": "Ar",
    "MKD": "ден",
    "MMK": "K",
    "MNT": "₮",
    "MOP": "P",
    "MRO": "UM",
    "MUR": "₨",
    "MVR": "ރ.",
    "MWK": "MK",
    "MXN": "$",
    "MYR": "RM",
    "MZN": "MT",
    "NAD": "$",
    "NGN": "₦",
    "NIO": "C$",
    "NOK": "kr",
    "NPR": "₨",
    "NZD": "$",
    "OMR": "ر.ع.",
    "PAB": "B/.",
    "PEN": "S/.",
    "PGK": "K",
    "PHP": "₱",
    "PKR": "₨",
    "PLN": "zł",
    "PYG": "₲",
    "QAR": "ر.ق",
    "RON": "RON",
    "RSD": "RSD",
    "RUB": "р.",
    "RWF": "Fr",
    "SAR": "ر.س",
    "SBD": "$",
    "SCR": "₨",
    "SDG": "S$",
    "SEK": "kr",
    "SGD": "$",
    "SHP": "£",
    "SLL": "Le",
    "SOS": "Sh",
    "SRD": "$",
    "STD": "Db",
    "SYP": "£, ل.س",
    "SZL": "L",
    "THB": "฿",
    "TJS": "ЅМ",
    "TMT": "m",
    "TND": "د.ت",
    "TOP": "T$",
    "TRY": "₤",
    "TTD": "$",
    "TWD": "$",
    "TZS": "Sh",
    "UAH": "₴",
    "UGX": "Sh",
    "USD": "$",
    "UYU": "$",
    "UZS": "лв",
    "VEF": "Bs",
    "VND": "₫",
    "VUV": "Vt",
    "WST": "T",
    "XAF": "Fr",
    "XCD": "$",
    "XOF": "Fr",
    "XPF": "Fr",
    "YER": "﷼",
    "ZAR": "R",
    "ZMK": "ZK",
    "ZWL": "$"
}


class GeonamesParseError(Exception):
    def __init__(self, message=None):
        # Call the base class constructor with the parameters it needs
        if not message:
            message = "I couldn't parse the Geonames file (http://download.geonames.org/export/dump/countryInfo.txt).  The format may have changed. An updated version of this software may be required, please check for updates and/or raise an issue on github."
        super(GeonamesParseError, self).__init__(message)


def update_geonames_data():
    """
    Parses the countries table from geonames.org, updating or adding records as needed.
    currency_symbol is not part of the countries table and is supplemented using the data
    obtained from the link provided in the countries table.
    :return: num_updated, num_created
    :raise GeonamesParseError:
    """
    r = requests.get('http://download.geonames.org/export/dump/countryInfo.txt', stream=True)
    data_headers = []
    num_created = 0
    num_updated = 0
    for line in r.iter_lines():
        line = line.decode()
        if line[0] == "#":
            if line[0:4] == "#ISO":
                data_headers = line.strip('# ').split('\t')
                if data_headers != DATA_HEADERS_ORDERED:
                    raise GeonamesParseError
            continue
        if not data_headers:
            raise GeonamesParseError
        bits = line.split('\t')

        data = {DATA_HEADERS_MAP[DATA_HEADERS_ORDERED[x]]: bits[x] for x in range(0, len(bits))}
        if data['currency_code']:
            data['currency_symbol'] = CURRENCY_SYMBOLS.get(data['currency_code'])

        clean_data = {x: y for x, y in data.items() if y}
        country, created = Country.objects.update_or_create(iso=clean_data['iso'], defaults=clean_data)
        if created:
            num_created += 1
        else:
            num_updated += 1
    return num_updated, num_created