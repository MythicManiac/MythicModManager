import os
import json

from ..thunderstore import ThunderstoreAPI


def test_api_data_loading():
    test_data_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "data", "api_sample.json"
    )
    with open(test_data_path, "r") as f:
        data = json.load(f)
    api = ThunderstoreAPI("http://localhost/")
    api.update_packages_with_data(data)
    assert len(api.get_package_names()) == len(data)
