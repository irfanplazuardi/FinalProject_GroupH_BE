teacher_schema = {
    'teacher_name': {
        'type': 'string',
        'required': True,
        'minlength': 1,
        'maxlength': 30,
        'regex': r'^[a-zA-Z\s]+$' 
    },
    'teacher_email': {
        'type': 'string',
        'required': True,
        'regex': r'^[^@]+@[^@]+\.[^@]+$', 
        'minlength': 5,
        'maxlength': 50
    },
    'teacher_birthday': {
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
        'type': 'blob', 
        'required': False 
    }
}

update_teacher_schema = {
    'teacher_name': {
        'type': 'string',
        'required': False,
        'minlength': 1,
        'maxlength': 30,
        'regex': r'^[a-zA-Z\s]+$' 
    },
    'teacher_email': {
        'type': 'string',
        'required': False,
        'regex': r'^[^@]+@[^@]+\.[^@]+$', 
        'minlength': 5,
        'maxlength': 50
    },
    'teacher_birthday': {
        'type': 'date',
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

