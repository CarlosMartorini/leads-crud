from flask import request, jsonify
from app.models.leads_model import Lead
from datetime import datetime
from app.configs.database import db

phone_validation = "^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"

def create_lead():
    data = request.get_json()

    data['creation_date'] = datetime.now()
    data['last_visit'] = datetime.now()
    data['visits'] = 1

    # TODO: tratar exceções do email e phone unicos => verificar o erro de retorno
    if Lead.query.filter(Lead.email == data['email']):
        return {'msg': f"The email {data['email']} already exists!"}
    
    if Lead.query.filter(Lead.phone == data['phone']):
        return {'msg': f"The phone {data['phone']} already exists!"}
    
    # TODO: phone obrigatório no formato (xx)xxxxx-xxxx usar regex
    if data['phone'] != phone_validation:
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


def get_all_leads():
    # TODO: deve ser ordenado pelo numero de visitas (maior para o menor)
    leads_list = Lead.query.all().order_by(Lead.visits.desc())

    # TODO: tratar exceção usando a lista estiver vázia
    if leads_list == []:
        return {'msg': 'The list is empty!'}


    return jsonify(leads_list), 200


def update_lead(id: int):
    ...
    # TODO: usar o email para encontrar o registro
    # TODO: acrescentar em 1 o numero de visitas 'visits'
    # TODO: atualizar a data de 'las_visit' para o momento do request
    # TODO: retorno vázio
    # TODO: corpo da requisição obrigatóriamente apenas com o email str
    # TODO: tratar exceção de nenhum registro encontrado


def delete_lead(id: int):
    ...
    # TODO: usar o email para encontrar o registro
    # TODO: retorno vázio
    # TODO: corpo da requisição obrigatóriamente apenas com o email str
    # TODO: tratar exceção de nenhum registro encontrado