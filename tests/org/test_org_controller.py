# -*- coding: utf-8 -*-

import pytest
from flask import g, current_app, url_for

from actionmanagementapp.org.org_models import Organization
from actionmanagementapp.utilities.resource_strings import OrganizationResourceStrings


def test_orgList(client, auth):
    with client:
        auth.login()  # login
        dbSession = current_app.config['DBSESSION']  # get the db session

        # when the user tries to see the page, a 200 response is set
        response200 = client.get(url_for('org.orgList'))
        assert response200.status_code == 200

        # -- if there is no organization in the list, assert that proper message is shown
        firstOrganization = dbSession.query(Organization).first()
        if firstOrganization is not None:  # if you find an organization, delete it
            dbSession.delete(firstOrganization)
            dbSession.commit()

        responseNoOrganizations = client.get(url_for('org.orgList'))
        # check that the proper message appears on screen
        assert g.organizationResourceStrings.TXT_NO_ORGANIZATIONS.encode('utf-8') \
               in responseNoOrganizations.data

        # add an organization in the organization list
        newOrganization = Organization()
        newOrganization.id = 1
        newOrganization.name = u'Δήμος Καλυμνίων'
        newOrganization.address = u'Πόθια'
        newOrganization.ceo = u'Ιωάννης Γαλουζής'
        dbSession.add(newOrganization)
        dbSession.commit()

        # check that the organization appears in the list
        responseOrganizations = client.get(url_for('org.orgList'))
        assert newOrganization.name.encode('utf-8') in responseOrganizations.data

        # delete the organization
        dbSession.delete(newOrganization)
        dbSession.commit()

def test_addOrg(client, auth):
    with client:
        auth.login()
        dbSession = current_app.config['DBSESSION']

        # check that the page exists
        response200 = client.get(url_for('org.addOrg'))
        assert response200.status_code == 200

        # -- check that the organization data are properly stored in the database
        newOrg = Organization()
        newOrg.id = 1000892
        newOrg.name = u'Δοκιμαστικό νομικό πρόσωπο'
        newOrg.type = 1
        newOrg.ceo = u'CEO Δοκιμαστικού νομικού προσώπου'
        newOrg.phone = u'+302243022711'
        newOrg.email = u'npdd@kalymnos.gr'
        newOrg.address = u'Χώρα Κάλυμνος 85200, Δωδεκάνησα, Ελλάδα'

        responsePost = client.post(url_for('org.addOrg'),
                                   data={
                                       'id': newOrg.id,
                                       'name': newOrg.name,
                                       'type': newOrg.type,
                                       'ceo': newOrg.ceo,
                                       'phone': newOrg.phone,
                                       'email': newOrg.email,
                                       'address': newOrg.address
                                   })
        # check that the http response is ok
        assert responsePost.status_code == 200

        # check that all fields have been properly stored in the database
        newOrgFromDatabase = dbSession.query(Organization)\
            .filter(Organization.id == newOrg.id).first()
        # check that all the data have been stored in the database
        assert (
                newOrg.id == newOrgFromDatabase.id and
                newOrg.name == newOrgFromDatabase.name and
                newOrg.type == newOrgFromDatabase.type and
                newOrg.parentOrganizationId == newOrgFromDatabase.parentOrganizationId and
                newOrg.ceo == newOrgFromDatabase.ceo and
                newOrg.address == newOrgFromDatabase.address and
                newOrg.email == newOrgFromDatabase.email and
                newOrg.phone == newOrgFromDatabase.phone
        )

        # delete the test organization
        dbSession.delete(newOrgFromDatabase)
        dbSession.commit()

@pytest.mark.parametrize(('name', 'ceo', 'errMessageName', 'errMessageCEO'), (
            (None, None,
             OrganizationResourceStrings.ERR_ORGANIZATION_EMPTY_NAME,
             OrganizationResourceStrings.ERR_ORGANIZATION_EMPTY_CEO),
    )
)
def test_addOrg_valid_fields(client, auth, name, ceo, errMessageName, errMessageCEO):
    """
    Function for field validation
    :param client:
    :param auth:
    :return:
    """
    with client:
        auth.login()
        dbSession = current_app.config['DBSESSION']

        responsePost = client.post(url_for('org.addOrg'),
                                   data={
                                       'name': name,
                                       'ceo': ceo
                                   })

        # check that the the error messages appear
        assert errMessageName.encode('utf-8') in responsePost.data
        assert errMessageCEO.encode('utf-8') in responsePost.data
