student_schema = {
    'student_name': {
        'type': 'string',
        'required': True,
        'minlength': 1,
        'maxlength': 30,
        'regex': r'^[a-zA-Z\s]+$'
    },
    'student_email': {
        'type': 'string',
        'required': True,
        'regex': r'^[^@]+@[^@]+\.[^@]+$', 
        'minlength': 5,
        'maxlength': 50
    },
    'student_birthday': {
        'type': ['date', 'string'],
        'required': True
    },
    'phone': {
        'type': 'string',
        'required': True,
        'minlength': 10,
        'maxlength': 20,
        'regex': r'^\+?[0-9\s]+$'
    },
    'password': {
        'type': 'string',
        'required': True,
        'minlength': 8,
        'maxlength': 255
    },
    'picture': {
        'type': ['string', 'binary'], 
        'required': False 
    }
}
