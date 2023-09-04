# create-server-profiles-with-reserved-WWPN-identifiers

`create-server-profiles-with-reserved-WWPN-identifiers` is a script to create Server Profiles from Server Profile Template with user-defined WWPN identifiers. Not all cases and exceptions are covered because the purpose of the script is to simply meet a basic need.

# Usage

First, the user has to retrieve Intersight API Keys from its account and paste them in a *.env* file in order to load them in the script.

Then, users can interact with the file `inventory_config.json` to craft the desired configurations. It is a JSON file made of the following parameters:

### Global Parameters:
- `organization` : Intersight Organization.
- `san_connectivity_policy` : SAN Connectivity Policy attached to the Server Profile Template.
- `server_profile_template` : Name of the Server Profile Template (source of the instantiated Server Profiles).
- `server_profiles`: List of Server Profiles to be created.

### Each Server Profile has the following attributes:
- `server_profile_name`: Name of the Server Profile.
- `reservations`: List of vHBAs attached to the Server Profile for which WWPN reservations will take place. The number of vHBAs is defined in the SAN Connectivity Policy.

### Each Reservation has the following attributes:
- `vhba_name`: Name of the vHBA.
- `wwpn_to_reserve`: Desired WWPN to be attached to the vHBA.
- `wwpn_pool`: Pool of vHBA.

### Finally, the user can execute the script with:
```
$ python main.py
```