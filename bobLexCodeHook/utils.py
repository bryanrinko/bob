import dateutil.parser

def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False