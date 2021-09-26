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

        # TODO: phone obrigatório no formato (xx)xxxxx-xxxx usar regex
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

    # TODO: tratar exceções do email e phone unicos => verificar o erro de retorno            
    except sqlalchemy.exc.IntegrityError as e:
        print(e.__dict__)
        return {'error': str(e.orig).split('\n')[1]}, 422


def get_all_leads():
    leads_list = Lead.query.all()

    # TODO: tratar exceção usando a lista estiver vázia
    if leads_list == []:
        return {'msg': 'The list is empty!'}, 200

    # TODO: deve ser ordenado pelo numero de visitas (maior para o menor)
    leads_list = sorted(leads_list, key=lambda item: item.visits)

    return jsonify(leads_list), 200


def update_lead():
    # TODO: corpo da requisição obrigatóriamente apenas com o email str
    data = request.get_json()

    try:
        # TODO: usar o email para encontrar o registro
        lead_to_update = Lead.query.filter_by(email=data['email']).one()
        print(lead_to_update)
        
        # TODO: atualizar a data de 'las_visit' para o momento do request
        lead_to_update.last_visit = datetime.now()

        # TODO: acrescentar em 1 o numero de visitas 'visits'
        lead_to_update.visits += 1

        current_app.db.session.commit()

        # TODO: retorno vázio
        return '', 200
    
    # TODO: tratar exceção de nenhum registro encontrado
    except sqlalchemy.exc.NoResultFound:
        return {'error': f"Could not find {data['email']} in the records!"}, 404
    
    except KeyError:
        return {'error': 'The request can only contain the email key'}, 404


def delete_lead():
    # TODO: corpo da requisição obrigatóriamente apenas com o email str
    data = request.get_json()

    try:
        # TODO: usar o email para encontrar o registro
        lead_to_delete = Lead.query.filter_by(email=data['email']).one()

        current_app.db.session.delete(lead_to_delete)
        current_app.db.session.commit()

        # TODO: retorno vázio
        return '', 200
    
    # TODO: tratar exceção de nenhum registro encontrado
    except sqlalchemy.exc.NoResultFound:
        return {'error': f"Could not find {data['email']} in the records!"}, 404

    except KeyError:
        return {'error': 'The request can only contain the email key'}, 404