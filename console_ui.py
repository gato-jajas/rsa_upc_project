# !!!ESTE ARCHIVO CONTIENE SOLO UI!!!
# (menu, input, output)

#   from core.math_utils import ...
#   from core.rsa_engine import ...
import os


# -----------------------------------------------------------
# funciones simuladas (placeholder de core.math y core.rsa)))
# -----------------------------------------------------------

def generar_claves(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # buscamos e que sea coprimo con phi, el primero que aparezca
    e = next(i for i in range(2, phi) if _mcd(i, phi) == 1)
    d = _inverso_modular(e, phi)

    return n, phi, e, d


def cifrar_mensaje(mensaje, e, n):
    # tabla A=0, B=1 ... Z=25, espacio=26
    tabla = {chr(65 + i): i for i in range(26)}
    tabla[' '] = 26

    resultado = []
    for c in mensaje.upper():
        if c in tabla:
            m = tabla[c]
            cifrado = pow(m, e, n)   # esto es C = M^e mod n
            resultado.append(cifrado)

    return resultado

def descifrar_mensaje(cifrados, d, n):
    inversa = {i: chr(65 + i) for i in range(26)}
    inversa[26] = ' '

    resultado = []
    for c in cifrados:
        m = pow(c, d, n)  # M = C^d mod n, magia del RSA
        resultado.append(inversa.get(m, '?'))

    return ''.join(resultado)


# helpers matematicos basicos (van a venir de math_utils despues)

def _mcd(a, b):
    while b:
        a, b = b, a % b
    return a

def _inverso_modular(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None  # si llega aqui algo salio mal xd


# ----------------
# output formating
# ----------------

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def separador(titulo=""):
    linea = "=" * 50
    if titulo:
        print(f"\n{linea}")
        print(f"  {titulo}")
        print(f"{linea}")
    else:
        print(linea)

def pausar():
    input("\n  Presiona Enter para continuar...")


def pedir_primo(nombre):
    # try/catch para input
    while True:
        try:
            valor = int(input(f"  Ingresa el primo {nombre}: "))

            if valor < 2:
                print("  no vale, tiene que ser mayor a 1")
                continue

            # chequeo (primos)
            if not all(valor % i != 0 for i in range(2, int(valor**0.5) + 1)):
                print(f"  {valor} no es primo, intenta con otro")
                continue

            return valor

        except ValueError:
            print("  eso no es un numero, intentalo de nuevo")


# -------------
# menu opciones
# ------------

def opcion_generar_claves(estado):
    separador("GENERAR CLAVES RSA")
    print("\n  necesitamos dos primos distintos, p y q\n")

    p = pedir_primo("p")
    q = pedir_primo("q")

    if p == q:
        print("\n  p y q tienen que ser distintos, no funciona con el mismo")
        pausar()
        return

    n, phi, e, d = generar_claves(p, q)

    print(f"\n  Primos          : p={p}, q={q}")
    print(f"  Modulo          : n = {p} x {q} = {n}")
    print(f"  Euler fi(n)     : ({p}-1)({q}-1) = {phi}")
    print(f"  Exp. publico    : e = {e}")
    print(f"  Exp. privado    : d = {d}")
    print(f"\n  clave publica  ->  (n={n}, e={e})")
    print(f"  clave privada  ->  (n={n}, d={d})")

    # guardar estado
    estado['n'] = n
    estado['e'] = e
    estado['d'] = d
    estado['claves_listas'] = True

    print("\n  listo, claves guardadas en sesion")
    pausar()


def opcion_cifrar(estado):
    separador("CIFRAR MENSAJE")

    if not estado.get('claves_listas'):
        print("\n  primero genera las claves con la opcion 1")
        pausar()
        return

    n, e = estado['n'], estado['e']
    print(f"\n  usando clave publica (n={n}, e={e})\n")

    mensaje = input("  mensaje (solo letras A-Z y espacios): ").upper()

    if not all(c.isalpha() or c == ' ' for c in mensaje):
        print("\n  solo letras y espacios por favor")
        pausar()
        return

    cifrados = cifrar_mensaje(mensaje, e, n)

    # print letra por letra
    print("\n  letra  ->  M   ->  C")
    print("  " + "-" * 22)
    tabla_inv = {chr(65 + i): i for i in range(26)}
    tabla_inv[' '] = 26
    for letra, c in zip(mensaje, cifrados):
        m = tabla_inv.get(letra, 26)
        print(f"    {letra}    ->  {m:2d}  ->  {c}")

    estado['ultimo_cifrado'] = cifrados
    print(f"\n  resultado: {cifrados}")
    pausar()


def opcion_descifrar(estado):
    separador("DESCIFRAR MENSAJE")

    if not estado.get('claves_listas'):
        print("\n  genera las claves primero (opcion 1)")
        pausar()
        return

    n, d = estado['n'], estado['d']
    print(f"\n  usando clave privada (n={n}, d={d})\n")

    if estado.get('ultimo_cifrado'):
        usar = input("  usar el ultimo mensaje cifrado? (s/n): ").lower()
        cifrados = estado['ultimo_cifrado'] if usar == 's' else pedir_lista_cifrados()
    else:
        cifrados = pedir_lista_cifrados()

    if cifrados is None:
        pausar()
        return

    resultado = descifrar_mensaje(cifrados, d, n)
    print(f"\n  mensaje original: {resultado}")
    pausar()


def pedir_lista_cifrados():
    try:
        raw = input("  ingresa los numeros cifrados separados por comas: ")
        return [int(x.strip()) for x in raw.split(',')]
    except ValueError:
        print("\n  formato invalido, ejemplo: 9, 14, 11")
        return None


def opcion_ver_estado(estado):
    separador("ESTADO DE LA SESION")

    if not estado.get('claves_listas'):
        print("\n  todavia no hay claves generadas")
    else:
        print(f"\n  n  (modulo)       = {estado['n']}")
        print(f"  e  (pub)          = {estado['e']}")
        print(f"  d  (priv)         = {estado['d']}")

        if estado.get('ultimo_cifrado'):
            print(f"  ultimo cifrado    = {estado['ultimo_cifrado']}")

    pausar()


def opcion_limpiar(estado):
    estado.clear()
    print("\n  sesion limpia, como nuevo")
    pausar()


# -------------------------------------------------------
# menu principal y loop
# -------------------------------------------------------

def mostrar_menu():
    separador("SISTEMA RSA  -  MA475 UPC")
    print("""
  [1] Generar claves RSA
  [2] Cifrar mensaje
  [3] Descifrar mensaje
  [4] Ver estado de sesion
  [5] Limpiar sesion
  [0] Salir
""")
    separador()


def main():
    estado = {}  # ultimo cifrado

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("  opcion: ").strip()

        if opcion == '1':
            opcion_generar_claves(estado)
        elif opcion == '2':
            opcion_cifrar(estado)
        elif opcion == '3':
            opcion_descifrar(estado)
        elif opcion == '4':
            opcion_ver_estado(estado)
        elif opcion == '5':
            opcion_limpiar(estado)
        elif opcion == '0':
            print("\n  chau!\n")
            break
        else:
            print("\n  esa opcion no existe")
            pausar()


if __name__ == "__main__":
    main()
