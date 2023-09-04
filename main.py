"""Main module to create Server Profiles from Template with pre-reserved identifiers."""
#!/usr/bin/env python3

import json
import os

from dotenv import load_dotenv
from intersight_api_functions import (
    helper_functions,
    intersight_api_methods,
    intersight_authentication,
)


##############################################################################
#                             Env Variables                                  #
##############################################################################


load_dotenv()

# Intersight
INTERSIGHT_KEY_ID = os.getenv("INTERSIGHT_KEY_ID")
INTERSIGHT_SECRET_KEY_PATH = os.getenv("INTERSIGHT_SECRET_KEY_PATH")

# Config gile
JSON_FILE = "inventory_config.json"


###############################################################################
#                                   Main                                      #
###############################################################################


if __name__ == "__main__":
    helper_functions.print_server_profiles_before_creation(JSON_FILE)

    # Create an API Client to Authenticate against Intersight using API Keys.
    api_client = intersight_authentication.authenticate_to_intersight(
        intersight_key_id=INTERSIGHT_KEY_ID,
        intersight_secret_key_path=INTERSIGHT_SECRET_KEY_PATH,
    )

    # Extract data from inventory_config JSON file.
    with open(JSON_FILE, "r", encoding="utf-8") as json_file:
        inventory_config = json.load(json_file)

    # Set parameters.
    organization_name = inventory_config["organization"]
    san_connectivity_policy_name = inventory_config["san_connectivity_policy"]
    server_profile_template_name = inventory_config["server_profile_template"]

    # Get Organization moid from Organization Name.
    organization_moid = (
        intersight_api_methods.get_organization_moid_from_organization_name(
            api_client=api_client, organization_name=organization_name
        )
    )

    # Get San Connectivity Policy moid from San Connectivity Policy Name.
    san_connectivity_policy_moid = intersight_api_methods.get_san_connectivity_policy_moid_from_san_connectivity_policy_name(
        api_client=api_client, san_connectivity_policy_name=san_connectivity_policy_name
    )

    # Get Server Profile Template moid from Server Profile Template Name.
    server_profile_template_moid = intersight_api_methods.get_server_profile_template_moid_from_server_profile_template_name(
        api_client=api_client, server_profile_template_name=server_profile_template_name
    )

    # Loop over the Server Profiles.
    for server_profile in inventory_config["server_profiles"]:
        server_profile_name = server_profile["server_profile_name"]
        server_profile_reservations = server_profile["reservations"]

        # Create a Server Profile from a Server Profile Template and Get moid of the new Server Profile.
        resp_create_server_profile_from_template = (
            intersight_api_methods.create_server_profile_from_template(
                api_client=api_client,
                organization_moid=organization_moid,
                server_profile_name=server_profile_name,
                server_profile_template_moid=server_profile_template_moid,
            )
        )

        new_server_profile_from_template_moid = (
            resp_create_server_profile_from_template.responses[0].body.moid
        )

        # Detach Server Profile from Server Profile Template.
        resp_detach_server_profile = (
            intersight_api_methods.detach_server_profile_from_template(
                api_client=api_client,
                server_profile_moid=new_server_profile_from_template_moid,
            )
        )

        # Detach San Connectivity Policy from Server Profile.
        resp_detach_san_connectivity_policy_from_server_profile = (
            intersight_api_methods.detach_san_connectivity_policy_from_server_profile(
                api_client=api_client,
                server_profile_moid=new_server_profile_from_template_moid,
                vnic_san_connectivity_policy_moid=san_connectivity_policy_moid,
            )
        )

        # Create WWPN reservations in WWPN Pools.
        for reservation in server_profile_reservations:
            # Get WWPN Pool moid from WWPN Pool Name.
            wwpn_pool_moid = (
                intersight_api_methods.get_wwpn_pool_moid_from_wwpn_pool_name(
                    api_client=api_client, wwpn_pool_name=reservation["wwpn_pool"]
                )
            )

            resp_create_fcpool_reservation = (
                intersight_api_methods.create_fcpool_reservation(
                    api_client=api_client,
                    organization_moid=organization_moid,
                    wwpn_pool_moid=wwpn_pool_moid,
                    wwpn_to_reserve=reservation["wwpn_to_reserve"],
                )
            )

            reservation["reservation_moid"] = resp_create_fcpool_reservation["moid"]

        # Associate FC Pool Reservations to Server Profile.
        resp_associate_fc_pool_reservations_to_server_profile = (
            intersight_api_methods.associate_fc_pool_reservations_to_server_profile(
                api_client=api_client,
                reservations=server_profile_reservations,
                server_profile_moid=new_server_profile_from_template_moid,
            )
        )

        # Attach San Connectivity Policy to Server Profile.
        resp_attach_san_connectivity_policy_from_server_profile = (
            intersight_api_methods.attach_san_connectivity_policy_from_server_profile(
                api_client=api_client,
                server_profile_moid=new_server_profile_from_template_moid,
                vnic_san_connectivity_policy_moid=san_connectivity_policy_moid,
            )
        )

        # Attach Server Profile to Server Profile Template.
        resp_attach_server_profile_to_server_profile_template = (
            intersight_api_methods.attach_server_profile_to_server_profile_template(
                api_client=api_client,
                server_profile_moid=new_server_profile_from_template_moid,
                server_profile_template_moid=server_profile_template_moid,
            )
        )
