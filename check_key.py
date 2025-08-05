import os

# Lee la variable de entorno
api_key = os.environ.get("OPENAI_API_KEY")

# Imprime la clave que Python está viendo
print("Python está viendo la siguiente clave de API:")
print(api_key)

if api_key:
    print("\n¡La variable de entorno está configurada! Si el error continúa, la clave es incorrecta.")
else:
    print("\nError: Python no puede encontrar la variable de entorno. Asegúrate de usar 'set OPENAI_API_KEY=...' en la misma terminal.")
