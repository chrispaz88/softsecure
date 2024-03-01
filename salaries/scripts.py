from phe import paillier
import json

def run():
    public_key, private_key = paillier.generate_paillier_keypair()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    # Convertir la clave pública a un diccionario y luego a una cadena JSON
    public_key_serialized = json.dumps({'n': public_key.n})
    # Convertir la clave privada a un diccionario y luego a una cadena JSON
    private_key_serialized = json.dumps({'p': private_key.p, 'q': private_key.q})

    # Guardar las claves serializadas en archivos
    with open('public_key.json', 'w') as public_key_file:
        public_key_file.write(public_key_serialized)

    with open('private_key.json', 'w') as private_key_file:
        private_key_file.write(private_key_serialized)


# Carga las claves desde donde las guardaste
