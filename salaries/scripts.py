from phe import paillier
import json

def run():
    public_key, private_key = paillier.generate_paillier_keypair()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    #Guarda la clave privada en un archivo
    with open('private_key.json', 'w') as private_key_file:
        private_key_data = {'p': private_key.p, 'q': private_key.q}
        json.dump(private_key_data, private_key_file)
    #Guarda la clave pública en un archivo
    with open('public_key.json', 'w') as public_key_file:
        public_key_data = {'n': public_key.n}
        json.dump(public_key_data, public_key_file)

#Funcion para carga la llave publica
def load_paillier_key_public():

    with open('public_key.json', 'r') as public_key_file:
        public_key_data = json.load(public_key_file)
        public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
    return public_key

#Funcion para carga la llave privada
def load_paillier_key_private():
    with open('private_key.json', 'r') as private_key_file:
        private_key_data = json.load(private_key_file)
        private_key = paillier.PaillierPrivateKey(public_key=load_paillier_key_public(),
                                                  p=int(private_key_data['p']),
                                                  q=int(private_key_data['q']))
    return private_key

def test():
    public_key, private_key = paillier.generate_paillier_keypair()
    secret_number = 1000
    #secret_number_list = [2,1, 1000]
    encrypted_number = public_key.encrypt(secret_number)
    #encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]
    print(f"Encrypted number: {encrypted_number}")
    cipher_sum = encrypted_number + encrypted_number
    cipher_encypted_number = encrypted_number.ciphertext()
    print(f"Encrypted number Cipher: {cipher_encypted_number}")

    #Proceso de desencriptación desde el cipher
    encrypted_number_after = paillier.EncryptedNumber(public_key, cipher_encypted_number)
    print(f"Encrypted number after: {encrypted_number_after}")
    decrypted_number = private_key.decrypt(encrypted_number_after)
    print(f"Decrypted number: {decrypted_number}")



    #[private_key.decrypt(x) for x in encrypted_number_list]
