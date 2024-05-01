announcement_schema = {
    'teacher_id': {
        'type': 'integer',
        'required': False
    },
    'announcement_desc': {
        'type': 'string',
        'required': True
    },
    'created_by': {
        'type': 'string',
        'required': False,
        'minlength': 1,
        'maxlength': 30
    }
}
