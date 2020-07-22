import json

import requests

from ep_operations.auth import external_login as login
from ep_operations.auth import external_logout as logout
from ep_operations.common import get_authorized_headers

GET_MODELS_V1_API = "{}/api/v1/production/models"


def get_models(uri: str, user: str, password: str, model_code: str = None):
    token = login(uri, user, password)
    if len(token) == 0:
        return

    headers = get_authorized_headers(token)

    endpoint = GET_MODELS_V1_API.format(uri)

    if model_code:
        endpoint += "/{}".format(model_code)

    get_models_api_request = requests.get(endpoint.format(uri), headers=headers)
    models_dict = get_models_api_request.json()

    if model_code:
        logout(uri, token)
        return print(json.dumps(__clean_model(models_dict.get("data")), indent=4))

    models = []
    for model in models_dict.get('rows', []):
        models.append(__clean_model(model))

    logout(uri, token)
    print(json.dumps(models, indent=4))


def __clean_model(model: dict):
    if not model:
        return {}

    out = {
        "id": model.get("id"),
        "image": model.get("image"),
        "name": model.get("name"),
        "tags": model.get("tags"),
        "application_bindings": [],
        "sensors": [],
        "actuators": []
    }

    actuators = model.get("actuators")
    for actuator in actuators:
        out["actuators"].append({
            "id": actuator.get("id"),
            "actuator_id": actuator.get("actuator_id"),
            "name": actuator.get("name"),
            "type": actuator.get("type"),
            "ack_type": actuator.get("ack_type"),
            "delta_flush": actuator.get("delta_flush"),
            "map": actuator.get("map"),
            "protocol": actuator.get("protocol")
        })

    sensors = model.get("sensors")
    for sensor in sensors:
        out["sensors"].append({
            "id": sensor.get("id"),
            "sensor_id": sensor.get("sensor_id"),
            "name": sensor.get("name"),
            "type": sensor.get("type"),
            "unit": sensor.get("unit"),
            "resend_equal": sensor.get("resend_equal"),
            "map": sensor.get("map"),
            "protocol": sensor.get("protocol")
        })

    apps = model.get("application_bindings")
    for app in apps:
        binding = {
            "id": app.get("id"),
            "auto_install": app.get("auto_install"),
        }
        application = app.get("applications")
        if application:
            binding["application"] = {
                "id": application.get("id"),
                "name": application.get("name"),
                "tags": application.get("tags"),
            }
        out["application_bindings"].append(binding)

    os_binding = model.get("os_binding")
    if os_binding:
        binding = {
            "id": os_binding.get("id"),
        }

        gw_model = os_binding.get("gateway_model")
        if gw_model:
            binding["gateway_model"] = {
                "id": gw_model.get("id"),
                "name": gw_model.get("name"),
                "vendor": gw_model.get("vendor")
            }

        os = os_binding.get("os")
        if os:
            binding["os"] = {
                "id": os.get("id"),
                "name": os.get("name"),
                "code_id": os.get("code_id")
            }
        out["os_binding"] = binding

    telemetry_provider = model.get("telemetry_provider")
    if telemetry_provider:
        out["telemetry_provider"] = {
            "id": telemetry_provider.get("id"),
            "name": telemetry_provider.get("name"),
            "code": telemetry_provider.get("code"),
        }

    return out
