course_schema = {
    'course_name': {
        'type': 'string',
        'required': True,
        'minlength': 1,
        'maxlength': 50
    },
    'course_subject_id': {
        'type': 'integer',
        'required': True
    },
    'course_description': {
        'type': 'string',
        'required': True
    },
    'course_grade': {
        'type': 'string',
        'allowed': ['SD', 'SMP', 'SMA'],
        'required': False
    },
    'picture': {
        'type': ['string', 'binary'], 
        'required': False 
    }
}

update_course_schema = {
    'course_name': {
        'type': 'string',
        'required': False ,
        'minlength': 1,
        'maxlength': 50
    },
    'course_subject_id': {
        'type': 'integer',
        'required': False
    },
    'course_description': {
        'type': 'string',
        'required': False
    },
    'picture': {
        'type': ['string', 'binary'], 
        'required': False 
    }
}