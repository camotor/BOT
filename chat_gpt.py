import openai
from openai import OpenAI
import os

# Inicializa el cliente de OpenAI
# La clave de API se toma automáticamente de la variable de entorno OPENAI_API_KEY
try:
    client = OpenAI()
except Exception as e:
    print(f"Error al inicializar el cliente de OpenAI: {e}")
    exit()

def main():
    """
    Función principal para interactuar con el modelo gpt-4o-mini.
    """
    print("\n¡Bienvenido al chat con gpt-4o-mini!")
    print("Escribe 'salir' cuando quieras terminar.\n")

    # Historial de la conversación
    conversation_history = []

    while True:
        # Lee la entrada del usuario
        user_input = input("Tú: ")

        # Condición para salir del bucle
        if user_input.lower() == 'salir':
            print("¡Hasta luego!")
            break

        # Agrega el mensaje del usuario al historial
        conversation_history.append({"role": "user", "content": user_input})

        try:
            # Llama a la API de OpenAI para obtener una respuesta
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history
            )

            # Extrae el mensaje de la respuesta
            bot_response = response.choices[0].message.content
            print(f"ChatGPT: {bot_response}")

            # Agrega la respuesta del bot al historial
            conversation_history.append({"role": "assistant", "content": bot_response})

        except openai.AuthenticationError:
            print("\nError de autenticación. Verifica que tu clave de API sea correcta.")
            print("Puedes configurar tu clave de API con el comando: set OPENAI_API_KEY=tu_clave_aqui")
            break
        except Exception as e:
            print(f"\nOcurrió un error: {e}")
            break

if __name__ == "__main__":
    main()
