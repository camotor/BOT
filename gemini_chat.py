import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    """
    Función principal para interactuar con el modelo Gemini.
    """
    # Carga las variables de entorno desde el archivo .env
    load_dotenv()

    # Intenta obtener la clave de API desde una variable de entorno
    api_key = os.environ.get("API_KEY_GEMINI")

    # Si no está en las variables de entorno, muestra un error y sale
    if not api_key or api_key == "YOUR_API_KEY":
        print("Error: La variable de entorno API_KEY_GEMINI no está configurada o no es válida.")
        print("Asegúrate de crear un archivo .env y añadir tu clave de API.")
        return

    # Configura la clave de API para la biblioteca de Gemini
    genai.configure(api_key=api_key)

    print("\n¡Bienvenido al chat con Gemini!")
    print("Escribe 'salir' cuando quieras terminar.\n")

    # Inicializa el modelo
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])

    while True:
        # Lee la entrada del usuario
        user_input = input("Tú: ")

        # Condición para salir del bucle
        if user_input.lower() == 'salir':
            print("¡Hasta luego!")
            break

        try:
            # Envía el mensaje al modelo y obtiene una respuesta
            response = chat.send_message(user_input)

            # Extrae el mensaje de la respuesta
            bot_response = response.text
            print(f"Gemini: {bot_response}")

        except Exception as e:
            print(f"\nOcurrió un error: {e}")
            break

if __name__ == "__main__":
    main()
