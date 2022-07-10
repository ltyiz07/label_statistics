
_ref_annotations = {
    "bsonType": "array",
    "items": {
        "bsonType": "object",
        "required": ["image_path", "image_id", "size", "objects"],
        "properties": {
            "image_path": {
                "description": "path from tar structure",
                "bsonType": "string"
            },
            "image_id": {
                "bsonType": "string"
            },
            "size": {
                "bsonType": "object",
                "description": "must be a string and is not required",
                "required": ["width", "height"],
                "properties": {
                    "width": {
                        "bsonType": "int"
                    },
                    "height": {
                        "bsonType": "int"
                    }
                }
            },
            "objects": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["name", "bndbox"],
                    "properties": {
                        "name": {
                            "bsonType": "string"
                        },
                        "bndbox": {
                            "bsonType": "object",
                            "required": ["xmin", "ymin", "xmax", "ymax"],
                            "properties": {
                                "xmin": {
                                    "bsonType": "string",
                                },
                                "ymin": {
                                    "bsonType": "string",
                                },
                                "xmax": {
                                    "bsonType": "string",
                                },
                                "ymax": {
                                    "bsonType": "string",
                                },
                            },
                        }
                    }
                }
            }
        }
    },
}

datasets_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["dataset_path", "dataset_id", "dataset_hash", "annotations"],
        "properties": {
            "dataset_path": {
                "bsonType": "string",
                "description": "tar file name"
            },
            "dataset_id": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "dataset_hash": {
                "bsonType": "string",
                "description": "generated from python, using size and date"
            },
            "annotations": _ref_annotations
        }
    }
}


if __name__ == "__main__":
    sample_datasets = {}
