# using Schemas is overkill for this project...
# instead use python class for database collection.

annotations_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["tar_path"],
        "properties": {
            "tar_path": {
                "bsonType": "string"
            }
        }
    }
}
datasets_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["tar_path"],
        "properties": {
            "tar_path": {
                "bsonType": "string"
            }
        }
    }
}

# annotations_schema = {
#     "$jsonSchema": {
#         "bsonType": "object",
#         "description": "label about single image",
#         "required": ["image_id", "dataset_id", "image_path", "size", "objects"],
#         "properties": {
#             "image_id": {
#                 "bsonType": "string"
#             },
#             "dataset_id": {
#                 "bsonType": "string"
#             },
#             "image_path": {
#                 "description": "path from tar structure",
#                 "bsonType": "string"
#             },
#             "size": {
#                 "bsonType": "object",
#                 "description": "must be a string and is not required",
#                 "required": ["width", "height"],
#                 "properties": {
#                     "width": {
#                         "bsonType": "int"
#                     },
#                     "height": {
#                         "bsonType": "int"
#                     }
#                 }
#             },
#             "objects": {
#                 "bsonType": "array",
#                 "items": {
#                     "bsonType": "object",
#                     "required": ["name", "bndbox"],
#                     "properties": {
#                         "name": {
#                             "bsonType": "string"
#                         },
#                         "bndbox": {
#                             "bsonType": "object",
#                             "required": ["xmin", "ymin", "xmax", "ymax"],
#                             "properties": {
#                                 "xmin": {
#                                     "bsonType": "string",
#                                 },
#                                 "ymin": {
#                                     "bsonType": "string",
#                                 },
#                                 "xmax": {
#                                     "bsonType": "string",
#                                 },
#                                 "ymax": {
#                                     "bsonType": "string",
#                                 },
#                             },
#                         }
#                     }
#                 }
#             }
#         }
#     }
# }

# datasets_schema = {
#     "$jsonSchema": {
#         "bsonType": "object",
#         "required": ["dataset_id", "dataset_path", "dataset_hash", "annotations"],
#         "properties": {
#             "dataset_id": {
#                 "bsonType": "string",
#                 "description": "must be a string and is required"
#             },
#             "dataset_path": {
#                 "bsonType": "string",
#                 "description": "tar file name"
#             },
#             "dataset_hash": {
#                 "bsonType": "string",
#                 "description": "generated from python, using size and date"
#             },
#             "annotations": {
#                 "bsonType": "array",
#                 "description": "list of annotation_ids",
#                 "items": {
#                     "bsonType": "string"
#                 }
#             }
#         }
#     }
# }
