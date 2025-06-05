from . import main
from flask import jsonify, request

from ..services.mask_service import mask_data


@main.route("/mask/pii", methods=["POST"])
def mask_pii():
    data = request.json
    strictness = data["strictness"] if "strictness" in data else "MEDIUM"
    masked_entities = data["mask_entity"] if "mask_entity" in data else None
    substitute = data["substitute"] if "substitute" in data else None
    record = data["data"] if "data" in data else None
    print("Data from mask_pii:", data)

    resp = mask_data(record, strictness=strictness, mask_entity=masked_entities, substitute=substitute)
    return jsonify(resp)