import os
import pytest
from test_inscription import devlobdd, req_connection, req_code_verif
from flask import session


def setup_account(client, devlobdd):
    devlobdd.delete_ja("timtonix@icloud.com")
    client.post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": "jesuisunebananeavecdespouvoirsmagiques"  # +12 caractères
    })
    code = devlobdd.get_code_via_jaid("8166")[1]
    req_code_verif(client, "JA-8166", code)
    req_connection(client, "timtonix@icloud.com", "jesuisunebananeavecdespouvoirsmagiques")


def test_editor_access_without_account(client):
    response = client.get('/home/editeur')
    assert response.status_code == 302


def test_good_editor_access(client, devlobdd):
    setup_account(client, devlobdd)
    response = client.get('/home/editeur')

    assert response.status_code == 200

def test_modify_site(client, devlobdd):
    response = client.post('/home/editeur', data={
        "titre": "test",
        "valeur1": "test",
        "valider": ""
    })

    assert response.status_code == 200