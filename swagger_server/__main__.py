#!/usr/bin/env python3

import connexion

from swagger_server import encoder


# Global in-memory data store
data_store = {}

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Fiatlink FLS01'}, pythonic_params=True)

    # Enable pretty-printing of JSON responses
    app.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True 

    app.run(port=8080)


if __name__ == '__main__':
    main()
