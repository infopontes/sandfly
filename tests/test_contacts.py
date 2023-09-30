import factory.fuzzy

from sandfly.models import Contact, ContactType


def test_create_contact(client, token):
    response = client.post(
        '/contacts/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'type_contact': 'email',
            'description': 'infopontes@gmail.com',
        },
    )
    assert response.json() == {
        'id': 1,
        'type_contact': 'email',
        'description': 'infopontes@gmail.com',
    }


def test_list_contacts(session, client, user, token):
    session.bulk_save_objects(ContactFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/contacts/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['contacts']) == 5


def test_list_contacts_pagination(session, user, client, token):
    session.bulk_save_objects(ContactFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/contacts/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['contacts']) == 2


def test_list_contacts_filter_contact_type(session, user, client, token):
    session.bulk_save_objects(
        ContactFactory.create_batch(
            5, user_id=user.id, type_contact=ContactType.email
        )
    )
    session.commit()

    response = client.get(
        '/contacts/?contact_type=email',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['contacts']) == 5


def test_list_contacts_filter_description(session, user, client, token):
    session.bulk_save_objects(
        ContactFactory.create_batch(
            5, user_id=user.id, description='description'
        )
    )
    session.commit()

    response = client.get(
        '/contacts/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['contacts']) == 5


def test_list_contacts_filter_combined(session, user, client, token):
    session.bulk_save_objects(
        ContactFactory.create_batch(
            5,
            user_id=user.id,
            type_contact=ContactType.email,
            description='combined description',
        )
    )

    session.bulk_save_objects(
        ContactFactory.create_batch(
            3,
            user_id=user.id,
            type_contact=ContactType.phone,
            description='other description',
        )
    )
    session.commit()

    response = client.get(
        '/contacts/?type_contact=email&description=combined',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['contacts']) == 5


def test_patch_contact_error(client, token):
    response = client.patch(
        '/contacts/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_contact(session, client, user, token):
    contact = ContactFactory(user_id=user.id)

    session.add(contact)
    session.commit()

    response = client.patch(
        f'/contacts/{contact.id}',
        json={'description': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json()['description'] == 'teste!'


def test_delete_contact(session, client, user, token):
    contact = ContactFactory(id=1, user_id=user.id)

    session.add(contact)
    session.commit()

    response = client.delete(
        f'/contacts/{contact.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json() == {
        'detail': 'Contact has been deleted successfully.'
    }


def test_delete_contact_error(client, token):
    response = client.delete(
        f'/contacts/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}


class ContactFactory(factory.Factory):
    class Meta:
        model = Contact

    type_contact = factory.fuzzy.FuzzyChoice(ContactType)
    description = factory.Faker('text')

    user_id = 1
