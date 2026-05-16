import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema
from pandera import Check

binary_check = Check.isin([-1, 0, 1])


data_schema_validation = DataFrameSchema(
    {
        "having_IP_Address": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "URL_Length": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Shortining_Service": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "having_At_Symbol": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "double_slash_redirecting": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Prefix_Suffix": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "having_Sub_Domain": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "SSLfinal_State": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Domain_registeration_length": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Favicon": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "port": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "HTTPS_token": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Request_URL": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "URL_of_Anchor": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Links_in_tags": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "SFH": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Submitting_to_email": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Abnormal_URL": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Redirect": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "on_mouseover": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "RightClick": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "popUpWidnow": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Iframe": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "age_of_domain": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "DNSRecord": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "web_traffic": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Page_Rank": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Google_Index": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Links_pointing_to_page": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Statistical_report": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
        "Result": Column(pa.Int64, checks=Check.isin([-1, 0, 1])),
    },
    strict=True,
    coerce=True
)