import argparse
import crypto
import fetch_data as wr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-kl", "--key_length", help="Длинна ключа", required = False)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',help='Запускает режим дешифрования') 
    args = parser.parse_args()

    path = wr.json_read("settings.json")
    system = crypto.HybridCryptosystem(key_size= int(args.key_length))
    if args.generation is not None:
        system.serialize_symmetric_key(path["symmetric_key"])
        system.serialize_public_key(path["public_key"])
        system.serialize_private_key(path["secret_key"])
    elif args.encryption is not None:
        text = wr.read_txt(path["initial_file"])
        system.deserialize_private_key(path["secret_key"])
        system.deserialize_symmetric_key(path["symmetric_key"])
        encrypt_text = system.encrypt(text)
        wr.write(path["encrypted_file"],encrypt_text)

    else:
        text = wr.read(path["encrypted_file"])
        system.deserialize_private_key(path["secret_key"])
        system.deserialize_symmetric_key(path["symmetric_key"])
        decrypt_text = system.decrypt(text)
        wr.write_txt(path["decrypted_file"],decrypt_text)