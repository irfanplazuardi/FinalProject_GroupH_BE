update_student_schema = {
    'student_name': {
        'type': 'string',
        'required': False,
        'minlength': 1,
        'maxlength': 30,
        'regex': r'^[a-zA-Z\s]+$'
    },
    'student_email': {
        'type': 'string',
        'required': False,
        'regex': r'^[^@]+@[^@]+\.[^@]+$', 
        'minlength': 5,
        'maxlength': 50
    },
    'student_birthday': {
        'type': ['date', 'string'],
        'required': False
    },
    'phone': {
        'type': 'string',
        'required': False,
        'minlength': 10,
        'maxlength': 20,
        'regex': r'^\+?[0-9\s]+$'
    },
    'password': {
        'type': 'string',
        'required': False,
        'minlength': 8,
        'maxlength': 255
    },
    'picture': {
        'type': ['string', 'binary'], 
        'required': False 
    }
}