INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text"
            },
            "sentiment": {
                "properties": {
                    "compound": {"type": "float"},
                    "neg": {"type": "float"},
                    "neu": {"type": "float"},
                    "pos": {"type": "float"},
                }
            }
        }
    }
}
