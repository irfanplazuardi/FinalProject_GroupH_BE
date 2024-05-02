from datetime import datetime
from cerberus import Validator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from models.teacher import Teacher
from models.announcement import Announcement
from connectors.mysql_connector import engine, db
from decorators.role_checker import role_required
from validations.announcement_schema import announcement_schema

announcement_routes = Blueprint('announcement_routes', __name__)

session = db.session

@announcement_routes.route('/announcement', methods=['GET'])
@login_required
@role_required('teacher', 'student')
def get_announcements():


    try:

        announcements = session.query(Announcement).all()

        response_data = {"announcements": [announcement.serialize() for announcement in announcements]}
        return jsonify(response_data), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing data"}), 500
    
    finally:
        session.close()


@announcement_routes.route('/announcement/<int:announcement_id>', methods=['GET'])
@login_required
@role_required('teacher', 'student')
def get_announcement(announcement_id):



    try:

        announcement = session.query(Announcement).filter(Announcement.announcement_id == announcement_id).first()
        if not announcement:
            return jsonify({"message": "Announcement not found"}), 404
        

        return jsonify({"announcement": announcement.serialize()}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing request data"}), 500
    
    finally:
        session.close()


@announcement_routes.route('/announcement', methods=['POST'])
@login_required
@role_required('teacher')
def create_announcement():

    v = Validator(announcement_schema)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400
    

    try:

        new_announcement = Announcement(
            teacher_id=current_user.teacher_id,
            announcement_desc=json_data['announcement_desc'],
            created_by=current_user.teacher_name
        )

        session.add(new_announcement)
        session.commit()

        return jsonify({"message": "New announcement created successfully"}), 201
    
    except IntegrityError as ie:
        session.rollback()
        print(f"Integrity Error: {ie}")
        return jsonify({"message": f"Integrity Error: {ie}"})
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": f"Failed to create new announcement: {e}"})
    
    finally:
        session.close()


@announcement_routes.route('/announcement/<int:announcement_id>', methods=['PUT'])
@login_required
@role_required('teacher')
def update_announcement(announcement_id):

    v = Validator(announcement_schema)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400
    

    try:

        announcement = session.query(Announcement).filter(Announcement.announcement_id == announcement_id).first()

        if not announcement:
            return jsonify({"message": "Announcement not found"}), 404

        announcement.announcement_desc = json_data.get('announcement_desc', announcement.announcement_desc)

        session.commit()
        return jsonify({"message": "Announcement updated successfully"}), 200
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Failed to update announcement: {e}"})
    
    finally:
        session.close()


@announcement_routes.route('/announcement/<int:announcement_id>', methods=['DELETE'])
@login_required
@role_required('teacher')
def delete_announcement(announcement_id):

    try:

        announcement = session.query(Announcement).filter(Announcement.announcement_id == announcement_id).first()
        
        if not announcement:
            return jsonify({"message": "Announcement not found"}), 404
        
        session.delete(announcement)
        session.commit()
        return jsonify({"message": "Announcement deleted successfully"}), 200
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Failed to delete announcement: {e}"})
    
    finally:
        session.close()