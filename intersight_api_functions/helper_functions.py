"""Module to print the Server Profiles to be created."""
#!/usr/bin/env python3

import json
from prettytable import PrettyTable

###############################################################################
#                                   Main                                      #
###############################################################################


def print_server_profiles_before_creation(inventory_config_file):
    """Print the Server Profiles to be created in tables so that the user can validate the parameters.

    Args:
        - inventory_config_file (String): Path to the configuration inventory JSON file.
    """
    # Extract data from inventory_config JSON file.
    with open(inventory_config_file, "r", encoding="utf-8") as json_file:
        inventory_config = json.load(json_file)

    # Set parameters.
    organization_name = inventory_config["organization"]
    san_connectivity_policy_name = inventory_config["san_connectivity_policy"]
    server_profile_template_name = inventory_config["server_profile_template"]
    server_profiles = inventory_config["server_profiles"]

    # Create the parameters table.
    table_parameters = PrettyTable()
    table_parameters.field_names = [
        "Server Profile Template",
        "San Connectivity Policy",
        "Organization",
    ]
    table_parameters.add_rows(
        [
            [
                server_profile_template_name,
                san_connectivity_policy_name,
                organization_name,
            ]
        ]
    )

    print("\nAll the Server Profiles will use the following parameters:\n")
    print(table_parameters)
    input1 = input("\nEnter 'y' to continue: ")

    # Create the Server Profiles table.
    if input1 == "y":
        for i, server_profile in enumerate(server_profiles):
            server_profile_name = server_profile["server_profile_name"]
            server_profile_reservations = server_profile["reservations"]

            table_server_profiles = PrettyTable()
            table_server_profiles.add_column("Server Profile", [server_profile_name])

            for j, server_profile_reservation in enumerate(server_profile_reservations):
                table_server_profiles.add_column(
                    f"vHBA {j}", [server_profile_reservation["vhba_name"]]
                )
                table_server_profiles.add_column(
                    f"WWPN of vHBA {j}",
                    [server_profile_reservation["wwpn_to_reserve"]],
                )

            print(f"\n{i+1}) The following Server Profile will be created:\n")
            print(table_server_profiles)
            input2 = input("\nEnter 'y' to continue: ")

            if input2 != "y":
                print("Skipping the creation.")
                exit()

    else:
        print("Skipping the creation.")
        exit()


###############################################################################
#                                   Main                                      #
###############################################################################


if __name__ == "__main__":
    pass
