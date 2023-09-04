"""Module providing functions to Create Server Profiles in Intersight."""
#!/usr/bin/env python3

import sys

import intersight
from intersight.model.bulk_mo_cloner import BulkMoCloner
from intersight.model.bulk_mo_merger import BulkMoMerger
from intersight.model.fcpool_reservation import FcpoolReservation
from intersight.model.mo_mo_ref import MoMoRef
from intersight.model.pool_reservation_reference import PoolReservationReference
from intersight.model.server_profile import ServerProfile
from intersight.model.server_profile_template import ServerProfileTemplate
from intersight.model.vnic_san_connectivity_policy import VnicSanConnectivityPolicy
from intersight.api import bulk_api, fcpool_api, organization_api, server_api, vnic_api


###############################################################################
#                           Get Org moid from Org Name                        #
###############################################################################


def get_organization_moid_from_organization_name(api_client, organization_name):
    """Get Organization moid from Organization name.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - organization_name (string): name of the Organization.

    Returns:
        - organization_moid (string) : moid of the Organization.
    """
    api_instance = organization_api.OrganizationApi(api_client)

    # Create filter.
    kwargs = dict(filter=f"Name eq {organization_name}")

    # Read a 'organization.Organization' resource with filter.
    try:
        organization_result = api_instance.get_organization_organization_list(**kwargs)
        organization_moid = organization_result.results[0].moid
        print(
            f"- Moid of the 0rganization {organization_name} is: {organization_moid}."
        )

        return organization_moid

    except intersight.ApiException as exception:
        print(
            f"Exception when calling OrganizationApi->get_organization_organization_list: {exception}\n"
        )
        sys.exit(1)


###############################################################################
#                           Get SPT moid from SPT Name                        #
###############################################################################


def get_server_profile_template_moid_from_server_profile_template_name(
    api_client, server_profile_template_name
):
    """Get Server Profile Template moid from Server Profile Template name.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - server_profile_template_name (string): name of the Server Profile Template.

    Returns:
        - server_profile_template_moid (moid) : moid of the Server Profile Template.
    """

    api_instance = server_api.ServerApi(api_client)

    # Create filter.
    kwargs = dict(filter=f"Name eq '{server_profile_template_name}'")

    # Read a 'server.ProfileTemplate' resource with filter.
    try:
        server_profile_template_result = api_instance.get_server_profile_template_list(
            **kwargs
        )
        server_profile_template_moid = server_profile_template_result.results[0].moid
        print(
            f"- Moid of the Server Profile Template {server_profile_template_name} is: {server_profile_template_moid}."
        )

        return server_profile_template_moid

    except intersight.ApiException as exception:
        print(
            f"Exception when calling ServerApi->get_server_profile_template_list: {exception}\n"
        )
        sys.exit(1)


###############################################################################
#                           Get SCP Moid from SCP Name                        #
###############################################################################


def get_san_connectivity_policy_moid_from_san_connectivity_policy_name(
    api_client, san_connectivity_policy_name
):
    """Get San Connectivity Policy moid from San Connectivity Policy name.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - san_connectivity_policy_name (string): name of the San Connectivity Policy.

    Returns:
        - san_connectivity_policy_moid (moid) : moid of the San Connectivity Policy.
    """

    api_instance = vnic_api.VnicApi(api_client)

    # Create filter.
    kwargs = dict(filter=f"Name eq '{san_connectivity_policy_name}'")

    # Read a 'vnic.SanConnectivityPolicy' resource. with filter.
    try:
        san_connectivity_policy_result = (
            api_instance.get_vnic_san_connectivity_policy_list(**kwargs)
        )
        san_connectivity_policy_moid = san_connectivity_policy_result.results[0].moid
        print(
            f"- Moid of the San Connectivity Policy {san_connectivity_policy_name} is: {san_connectivity_policy_moid}."
        )

        return san_connectivity_policy_moid

    except intersight.ApiException as exception:
        print(
            f"Exception when calling VnicApi->get_vnic_san_connectivity_policy_list: {exception}\n"
        )
        sys.exit(1)


###############################################################################
#                           Create Server Profile                             #
###############################################################################


def create_server_profile(api_client, organization_moid, server_profile_name):
    """Create a Server Profile in a defined Organization.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - organization_moid (string): moid of the Organization.
        - server_profile_name (string): name of the Server Profile.

    Returns:
        - resp_create_server_profile
    """
    api_instance = server_api.ServerApi(api_client)

    # Create 'Organization' object.
    organization = MoMoRef(
        object_type="organization.Organization",
        moid=organization_moid,
    )

    # 'ServerProfile' | The 'server.Profile' resource to create.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile instance.
    server_profile.name = server_profile_name
    server_profile.organization = organization

    try:
        # Create a 'server.Profile' resource.
        resp_create_server_profile = api_instance.create_server_profile(
            server_profile=server_profile
        )
        print(f"- Creating Server Profile: {server_profile_name}.")

        return resp_create_server_profile

    except intersight.ApiException as exception:
        print(f"Exception when calling ServerApi->create_server_profile: {exception}\n")
        sys.exit(1)


###############################################################################
#                    Create Server Profile from Template                      #
###############################################################################


def create_server_profile_from_template(
    api_client, organization_moid, server_profile_name, server_profile_template_moid
):
    """Create a Server Profile from a Server Profile Template.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - organization_moid (string): moid of the Organization.
        - server_profile_name (string): name of the Server Profile.
        - server_profile_template_moid (string): moid of the Server Profile Template source.

    Returns:
        - resp_create_server_profile_from_template
    """
    api_instance = bulk_api.BulkApi(api_client)

    # Create 'Organization' object.
    organization = MoMoRef(
        object_type="organization.Organization",
        moid=organization_moid,
    )

    # 'BulkMoCloner' | The 'bulk.MoCloner' resource to create.
    server_profile_from_template = BulkMoCloner()

    # Create 'ServerProfileTemplate' object and 'ServerProfile' object.
    server_profile_template = ServerProfileTemplate(moid=server_profile_template_moid)
    server_profile = ServerProfile(name=server_profile_name, organization=organization)

    # Create 'Sources' object with inner server_profile_template instance.
    sources = [server_profile_template]

    # Create 'Targets' object with inner server_profile instance.
    targets = [server_profile]

    # Setting all the attributes for server_profile_from_template instance.
    server_profile_from_template.sources = sources
    server_profile_from_template.targets = targets

    try:
        # Create a 'bulk.MoCloner' resource.
        resp_create_server_profile_from_template = api_instance.create_bulk_mo_cloner(
            server_profile_from_template
        )
        print(
            f"- Creating Server Profile {server_profile_name} from Server Profile Template {server_profile_template_moid}."
        )

        return resp_create_server_profile_from_template

    except intersight.ApiException as exception:
        print(f"Exception when calling BulkApi->create_bulk_mo_cloner: {exception}\n")
        sys.exit(1)


###############################################################################
#                    Detach Server Profile from Template                      #
###############################################################################


def detach_server_profile_from_template(api_client, server_profile_moid):
    """Detach a Server Profile from a Server Profile Template.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - server_profile_moid (string): moid of the Server Profile.

    Returns:
        - resp_detach_server_profile
    """
    api_instance = server_api.ServerApi(api_client)

    # 'ServerProfile' | The 'server.Profile' resource to update.
    server_profile = ServerProfile(moid=server_profile_moid)

    # Updating attribute src_template object of server_profile instance to None.
    server_profile.src_template = None

    try:
        # Update a 'server.Profile' resource.
        resp_detach_server_profile = api_instance.update_server_profile(
            server_profile=server_profile, moid=server_profile_moid
        )
        print(
            f"- Detaching Server Profile {server_profile_moid} from Server Profile Template."
        )

        return resp_detach_server_profile

    except intersight.ApiException as exception:
        print(f"Exception when calling ServerApi->update_server_profile: {exception}\n")
        sys.exit(1)


###############################################################################
#                         Get San Connectivity Policy                         #
###############################################################################


def get_san_connectivity_policy_by_moid(api_client, vnic_san_connectivity_policy_moid):
    """Get San Connectivity Policy from its moid.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - vnic_san_connectivity_policy_moid (string): moid of San Connectivity Policy.

    Returns:
        - resp_get_vnic_san_connectivity_policy_by_moid
    """
    api_instance = vnic_api.VnicApi(api_client)

    try:
        # Read a 'vnic.SanConnectivityPolicy' resource.
        resp_get_vnic_san_connectivity_policy_by_moid = (
            api_instance.get_vnic_san_connectivity_policy_by_moid(
                moid=vnic_san_connectivity_policy_moid
            )
        )
        print(resp_get_vnic_san_connectivity_policy_by_moid)

        return resp_get_vnic_san_connectivity_policy_by_moid

    except intersight.ApiException as exception:
        print(
            f"Exception when calling VnicApi->get_vnic_san_connectivity_policy_by_moid: {exception}\n"
        )
        sys.exit(1)


###############################################################################
#              Detach San Connectivity Policy from Server Profile             #
###############################################################################


def detach_san_connectivity_policy_from_server_profile(
    api_client, vnic_san_connectivity_policy_moid, server_profile_moid
):
    """Detach a San Connectivity Policy from a Server Profile.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - server_profile_moid (string): moid of the Server Profile.
        - vnic_san_connectivity_policy_moid (string): moid of San Connectivity Policy.

    Returns:
        - resp_detach_san_connectivity_policy_from_server_profile
    """
    api_instance = vnic_api.VnicApi(api_client)

    try:
        # Read a 'vnic.SanConnectivityPolicy' resource.
        resp_get_vnic_san_connectivity_policy_by_moid = (
            api_instance.get_vnic_san_connectivity_policy_by_moid(
                moid=vnic_san_connectivity_policy_moid
            )
        )

    except intersight.ApiException as exception:
        print(
            f"Exception when calling VnicApi->get_vnic_san_connectivity_policy_by_moid: {exception}\n"
        )
        sys.exit(1)

    # Update the 'Profiles' object of the fetched vnic_san_connectivity_policy instance.
    profiles = resp_get_vnic_san_connectivity_policy_by_moid.profiles
    profiles = [
        profile for profile in profiles if profile.get("moid") != server_profile_moid
    ]

    # 'VnicSanConnectivityPolicy' | The 'vnic.SanConnectivityPolicy' resource to update.
    vnic_san_connectivity_policy = VnicSanConnectivityPolicy(
        moid=vnic_san_connectivity_policy_moid
    )

    # Update 'Profiles' object of vnic_san_connectivity_policy instance.
    vnic_san_connectivity_policy.profiles = profiles

    try:
        # Update a 'vnic.SanConnectivityPolicy' resource.
        resp_detach_san_connectivity_policy_from_server_profile = (
            api_instance.update_vnic_san_connectivity_policy(
                vnic_san_connectivity_policy=vnic_san_connectivity_policy,
                moid=vnic_san_connectivity_policy_moid,
            )
        )
        print(
            f"- Detaching San Connectivity Policy {vnic_san_connectivity_policy_moid} from Server Profile {server_profile_moid}."
        )

        return resp_detach_san_connectivity_policy_from_server_profile

    except intersight.ApiException as exception:
        print(
            f"Exception when calling VnicApi->update_vnic_san_connectivity_policy: {exception}\n"
        )
        sys.exit(1)


###############################################################################
#                     Get WWPN Pool moid from WWPN Pool name                  #
###############################################################################


def get_wwpn_pool_moid_from_wwpn_pool_name(api_client, wwpn_pool_name):
    """Get moid of WWPN Pool from its name.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - wwpn_pool_name (string): name of the WWPN Pool.

    Returns:
        - wwpn_pool_moid (string): moid of the WWPN Pool.
    """
    api_instance = fcpool_api.FcpoolApi(api_client)

    # Create filter.
    kwargs = dict(filter=f"Name eq '{wwpn_pool_name}'")

    # Read a 'fcpool.Pool' resource with filter.
    try:
        wwpn_pool_result = api_instance.get_fcpool_pool_list(**kwargs)
        wwpn_pool_moid = wwpn_pool_result.results[0].moid
        print(f"- Moid of the WWPN Pool {wwpn_pool_name} is: {wwpn_pool_moid}.")

        return wwpn_pool_moid

    except intersight.ApiException as exception:
        print(f"Exception when calling FcpoolApi->get_fcpool_pool_list: {exception}\n")
        sys.exit(1)


###############################################################################
#                       Create FC Pool Reservations                           #
###############################################################################


def create_fcpool_reservation(
    api_client, organization_moid, wwpn_pool_moid, wwpn_to_reserve
):
    """Create a WWPN reservation in a WWPN Pool.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - organization_moid (string): moid of the Organization.
        - wwpn_pool_moid (string): moid of the WWPN Pool.
        - wwpn_to_reserve (string): WWPN to reserve.

    Returns:
        - resp_create_fcpool_reservation
    """
    api_instance = fcpool_api.FcpoolApi(api_client)

    # Create 'Organization' object.
    organization = MoMoRef(
        object_type="organization.Organization",
        moid=organization_moid,
    )

    # 'FcpoolReservation' | The 'fcpool.Reservation' resource to create.
    fcpool_reservation = FcpoolReservation()

    # Create 'fcpool.Pool' object.
    wwpn_pool = MoMoRef(object_type="fcpool.Pool", moid=wwpn_pool_moid)

    # Setting all the attributes for fcpool_reservation instance.
    fcpool_reservation.allocation_type = "dynamic"
    fcpool_reservation.identity = wwpn_to_reserve
    fcpool_reservation.id_purpose = "WWPN"
    fcpool_reservation.organization = organization
    fcpool_reservation.pool = wwpn_pool

    try:
        # Create a 'fcpool.Reservation' resource.
        resp_create_fcpool_reservation = api_instance.create_fcpool_reservation(
            fcpool_reservation=fcpool_reservation
        )
        print(
            f"- Creating a WWPN reservation for WWPN {wwpn_to_reserve} in WWPN Pool {wwpn_pool_moid}."
        )

        return resp_create_fcpool_reservation

    except intersight.ApiException as exception:
        print(
            f"Exception when calling FcpoolApi->create_fcpool_reservation: {exception}\n"
        )
        sys.exit(1)


###############################################################################
#              Associate FC Pool Reservations to Server Profile               #
###############################################################################


def associate_fc_pool_reservations_to_server_profile(
    api_client, reservations, server_profile_moid
):
    """Associate FC Pool Reservations to Server Profile.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - reservations (list of dictionnaries): object used to describe FC Pool Reservations. It has for format the following structure:
            reservations = [{"vhba_name": "vhba_name","wwpn_to_reserve": "wwpn_to_reserve","wwpn_pool": "wwpn_pool","reservation_moid": "reservation_moid"},...]
        - server_profile_moid (string): moid of the Server Profile.

    Returns:
        - resp_associate_fc_pool_reservations_to_server_profile
    """
    api_instance = server_api.ServerApi(api_client)

    # 'ServerProfile' | The 'server.Profile' resource to update.
    server_profile = ServerProfile(moid=server_profile_moid)

    # Create 'FcpoolReservationReference' object.
    server_profile.reservation_references = []
    for reservation in reservations:
        fcpool_reservation_reference = PoolReservationReference(
            object_type="fcpool.ReservationReference",
            class_id="fcpool.ReservationReference",
            consumer_type="Vhba",
            consumer_name=reservation["vhba_name"],
            reservation_moid=reservation["reservation_moid"],
        )

        # Update attribute reservation_references of server_profile instance
        server_profile.reservation_references.append(fcpool_reservation_reference)

    try:
        # Update a 'server.Profile' resource.
        resp_associate_fc_pool_reservations_to_server_profile = (
            api_instance.update_server_profile(
                server_profile=server_profile, moid=server_profile_moid
            )
        )
        print(
            f"- Associating FC Pool Reservations to Server Profile {server_profile_moid}."
        )

        return resp_associate_fc_pool_reservations_to_server_profile

    except intersight.ApiException as exception:
        print(f"Exception when calling ServerApi->update_server_profile: {exception}\n")
        sys.exit(1)


###############################################################################
#                Attach San Connectivity Policy to Server Profile             #
###############################################################################


def attach_san_connectivity_policy_from_server_profile(
    api_client, server_profile_moid, vnic_san_connectivity_policy_moid
):
    """Attach a San Connectivity Policy to Server Profile.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - server_profile_moid (string): moid of the Server Profile.
        - vnic_san_connectivity_policy_moid (string): moid of the San Connectivity Policy.

    Returns:
        - resp_attach_san_connectivity_policy_from_server_profile
    """
    api_instance = vnic_api.VnicApi(api_client)

    try:
        # Read a 'vnic.SanConnectivityPolicy' resource.
        resp_get_vnic_san_connectivity_policy_by_moid = (
            api_instance.get_vnic_san_connectivity_policy_by_moid(
                moid=vnic_san_connectivity_policy_moid
            )
        )

    except intersight.ApiException as exception:
        print(
            f"Exception when calling VnicApi->get_vnic_san_connectivity_policy_by_moid: {exception}\n"
        )
        sys.exit(1)

    # 'VnicSanConnectivityPolicy' | The 'vnic.SanConnectivityPolicy' resource to update.
    vnic_san_connectivity_policy = VnicSanConnectivityPolicy(
        moid=vnic_san_connectivity_policy_moid
    )

    # Create 'server.Profile' object.
    profile = MoMoRef(object_type="server.Profile", moid=server_profile_moid)

    # Append 'server.Profile' object to 'Profiles' object of vnic_san_connectivity_policy instance.
    profiles = resp_get_vnic_san_connectivity_policy_by_moid.profiles
    profiles.append(profile)
    vnic_san_connectivity_policy.profiles = profiles

    try:
        # Update a 'vnic.SanConnectivityPolicy' resource.
        resp_attach_san_connectivity_policy_from_server_profile = (
            api_instance.update_vnic_san_connectivity_policy(
                vnic_san_connectivity_policy=vnic_san_connectivity_policy,
                moid=vnic_san_connectivity_policy_moid,
            )
        )
        print(
            f"- Attaching San Connectivity Policy {vnic_san_connectivity_policy_moid} to Server Profile {server_profile_moid}."
        )

        return resp_attach_san_connectivity_policy_from_server_profile

    except intersight.ApiException as exception:
        print(
            f"Exception when calling VnicApi->update_vnic_san_connectivity_policy: {exception}\n"
        )
        sys.exit(1)


###############################################################################
#                Attach Server Profile to Server Profile Template             #
###############################################################################


def attach_server_profile_to_server_profile_template(
    api_client, server_profile_moid, server_profile_template_moid
):
    """Attach a Server Profile to Server Profile Template.

    Args:
        - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
        - server_profile_moid (string): moid of the Server Profile.
        - server_profile_template_moid (string): moid of the Server Profile Template.

    Returns:
        - resp_attach_server_profile_to_server_profile_template
    """
    ### Bulk Mo Merger ###
    api_instance = bulk_api.BulkApi(api_client)

    # 'BulkMoMerger' | The 'bulk.MoMerger' resource to create.
    server_profile_attached_to_template = BulkMoMerger()

    # Create 'ServerProfileTemplate' object and 'ServerProfile' object.
    server_profile_template = ServerProfileTemplate(moid=server_profile_template_moid)
    server_profile = ServerProfile(moid=server_profile_moid)

    # Create 'Sources' object with inner server_profile_template instance.
    sources = [server_profile_template]

    # Create 'Targets' object with inner server_profile instance.
    targets = [server_profile]

    # Setting all the attributes for server_profile_attached_to_template instance.
    server_profile_attached_to_template.merge_action = "Replace"
    server_profile_attached_to_template.sources = sources
    server_profile_attached_to_template.targets = targets

    try:
        # Create a 'bulk.MoMerger' resource.
        resp_attach_server_profile_to_server_profile_template_mo_merger = (
            api_instance.create_bulk_mo_merger(
                bulk_mo_merger=server_profile_attached_to_template
            )
        )

    except intersight.ApiException as exception:
        print(f"Exception when calling BulkApi->create_bulk_mo_merger: {exception}\n")
        sys.exit(1)

    ### Update Server Profile ###
    api_instance = server_api.ServerApi(api_client)

    # 'ServerProfile' | The 'server.Profile' resource to update.
    server_profile = ServerProfile(moid=server_profile_moid)

    # Create 'ServerProfileTemplate' object and 'ServerProfile' object.
    server_profile_template = MoMoRef(
        object_type="server.ProfileTemplate", moid=server_profile_template_moid
    )

    # Update 'src_template' object of server_profile instance.
    server_profile.src_template = server_profile_template

    try:
        # Update a 'server.Profile' resource.
        resp_attach_server_profile_to_server_profile_template = (
            api_instance.update_server_profile(
                server_profile=server_profile, moid=server_profile_moid
            )
        )
        print(
            f"- Attaching Server Profile {server_profile_moid} to Server Profile Template {server_profile_template_moid}."
        )

        return resp_attach_server_profile_to_server_profile_template

    except intersight.ApiException as exception:
        print(f"Exception when calling ServerApi->update_server_profile: {exception}\n")
        sys.exit(1)


##############################################################################
#                                   Main                                     #
##############################################################################

if __name__ == "__main__":
    pass
