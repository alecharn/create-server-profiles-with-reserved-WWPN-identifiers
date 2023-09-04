"""Module providing functions to Authenticate to Intersight."""
#!/usr/bin/env python3

import datetime
import intersight
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


##############################################################################
#                   Authentication Scheme for Intersight                     #
##############################################################################


def authenticate_to_intersight(intersight_key_id, intersight_secret_key_path):
    """Authenticate to Cisco Intersight with Key ID and Secret Key from Cisco Intersight API.

    Args:
    - intersight_key_id (string): Cisco Intersight API Key ID.
    - intersight_secret_key_path (string): Path to the Cisco Intersight API Private Key.

    Returns:
    - api_client (Intersight ApiClient object): ApiClient object used to communicate with the Intersight server.
    """
    configuration = intersight.Configuration(
        host="https://intersight.com",
        signing_info=intersight.signing.HttpSigningConfiguration(
            key_id=intersight_key_id,
            private_key_path=intersight_secret_key_path,
            # For OpenAPI v2
            # signing_scheme=intersight.signing.SCHEME_RSA_SHA256,
            # For OpenAPI v3
            signing_scheme=intersight.signing.SCHEME_HS2019,
            # For OpenAPI v2
            # signing_algorithm=intersight.signing.ALGORITHM_RSASSA_PKCS1v15,
            # For OpenAPI v3
            signing_algorithm=intersight.signing.ALGORITHM_ECDSA_MODE_FIPS_186_3,
            signed_headers=[
                intersight.signing.HEADER_REQUEST_TARGET,
                intersight.signing.HEADER_CREATED,
                intersight.signing.HEADER_EXPIRES,
                intersight.signing.HEADER_HOST,
                intersight.signing.HEADER_DATE,
                intersight.signing.HEADER_DIGEST,
                "Content-Type",
                "User-Agent",
            ],
            signature_max_validity=datetime.timedelta(minutes=5),
        ),
    )

    # This is required in case of an API mismatch between Intersight and the SDK. It will allow the SDK to work.
    # with a higher version of the API (unknown attributes) without raising exceptions.
    configuration.discard_unknown_keys = True

    configuration.disabled_client_side_validations = "minimum"

    configuration.verify_ssl = False

    api_client = intersight.ApiClient(configuration)
    api_client.set_default_header("Content-Type", "application/json")

    return api_client


##############################################################################
#                                   Main                                     #
##############################################################################

if __name__ == "__main__":
    pass
