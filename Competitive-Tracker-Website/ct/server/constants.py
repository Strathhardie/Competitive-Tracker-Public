import os

CONSTANTS = {
    'PORT': os.environ.get('PORT', 3001),
    'HTTP_STATUS': {
        '404_NOT_FOUND': 404,
    },
    'ENDPOINT': {
        'MASTER_DETAIL': '/api/masterdetail',
    },
    'USERNAME': 'competitivetracker',
    'PASSWORD': 'pbkdf2:sha256:150000$Me4gX5PX$58fd2032897ddca334594ea367d6c128e091a806a76e6abb97e27712060305c3',
}
