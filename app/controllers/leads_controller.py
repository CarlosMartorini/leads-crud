from operator import itemgetter
from re import fullmatch
from flask import request, jsonify, current_app
import sqlalchemy
from app.models.leads_model import Lead
from datetime import datetime
from app.configs.database import db

phone_validation = "^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"

def create_lead():
    data = request.get_json()

    try:
        data['creation_date'] = datetime.now()
        data['last_visit'] = datetime.now()
        data['visits'] = 1

        if fullmatch(phone_validation, data['phone']):
            return {'msg': f"The phone must be like (xx)xxxxx-xxxx and you try pass {data['phone']}"}

        new_lead = Lead(**data)

        db.session.add(new_lead)
        db.session.commit()

        return {
            "name": data['name'],
            "email": data['email'],
            "phone": data['phone'],
            "creation_date": data['creation_date'],
            "last_visit": data['last_visit'],
            "visits": data['visits']
        }, 201

    except sqlalchemy.exc.IntegrityError as e:
        print(e.__dict__)
        return {'error': str(e.orig).split('\n')[1]}, 422


def get_all_leads():
    leads_list = Lead.query.all()

    if leads_list == []:
        return {'msg': 'The list is empty!'}, 200

    leads_list = sorted(leads_list, key=lambda item: item.visits)

    return jsonify(leads_list), 200


def update_lead():
    data = request.get_json()

    try:
        lead_to_update = Lead.query.filter_by(email=data['email']).one()
        
        lead_to_update.last_visit = datetime.now()

        lead_to_update.visits += 1

        current_app.db.session.commit()

        return '', 200
    
    except sqlalchemy.exc.NoResultFound:
        return {'error': f"Could not find {data['email']} in the records!"}, 404
    
    except KeyError:
        return {'error': 'The request can only contain the email key'}, 404


def delete_lead():
    data = request.get_json()

    try:
        lead_to_delete = Lead.query.filter_by(email=data['email']).one()

        current_app.db.session.delete(lead_to_delete)
        current_app.db.session.commit()

        return '', 200
    
    except sqlalchemy.exc.NoResultFound:
        return {'error': f"Could not find {data['email']} in the records!"}, 404

    except KeyError:
        return {'error': 'The request can only contain the email key'}, 404