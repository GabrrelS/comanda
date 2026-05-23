import bcrypt

def gerar_hash(senha):

    senha_bytes = senha.encode('utf-8')

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(
        senha_bytes,
        salt
    ).decode('utf-8')


def verificar(
    senha,
    hash_senha
):

    return bcrypt.checkpw(

        senha.encode('utf-8'),

        hash_senha.encode('utf-8')
    )