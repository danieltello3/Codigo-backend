

# funcion para personalizar el mensaje de error de mi libreria de JWT
def manejo_error_JWT(error):
    print(error)
    print(type(error))
    print(error.status_code)
    print(error.description)
    print(error.headers)
    respuesta = {
        "success": False,
        "content": None,
        "message": None
    }

    if error.error == 'Authorization Required':
        respuesta['message'] = "Se necesita una token para esta peticion"
    elif error.error == 'Bad Request':
        respuesta['message'] = "Credenciales invalidas"
    elif error.description == 'Signature has expired':
        respuesta['message'] = "Token ya expiro"
    elif error.description == 'Signature verification failed':
        respuesta['message'] = "Token invalida"
    elif error.description == 'Unsupported authorization type':
        respuesta['message'] = "tipo de autorizacion invalida, debe mandar JWT"
    else:
        respuesta['message'] = "error desconocido"

    return respuesta, error.status_code
    # 401 => unauthorized
