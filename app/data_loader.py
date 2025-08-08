import os
import pdfplumber


def load_data():
    """
    Loads data from a PDF file and organizes it into sections.
    Each section is identified by a title that starts with a number.
    """
    try:
      data= []
      current_section=""
      current_title=""

      # Abrir el archivo PDF
      with pdfplumber.open(os.path.join("data", "Gym_dream.pdf")) as pdf:

        # Dividir el PDF en páginas y extraer texto
        text = ""
        for page in pdf.pages:
          text += page.extract_text() + "\n"
        
        # Dividir el texto en secciones por líneas
        sections=text.split("\n")

        # Procesar cada línea
        for line in sections:
          line = line.strip()
          if line:
            # Si la línea comienza con un número, es un título de sección
            if line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.")):
              #Si hay una sección actual, agregarla a los datos
              if current_section:
                data.append({
                    "title": current_title,
                    "content": f"{current_title}\n{current_section.strip()}"
                })
              # Iniciar una nueva sección
              current_title = line
              current_section = ""
            else:
              # Agregar contenido a la sección actual
              current_section += line + "\n"
        
      # Agregar la última sección si existe
        if current_section:
          data.append({
              "title": current_title,
              "content": current_section.strip()
          })

      # Imprimir las secciones procesadas
      print("\n=== Secciones procesadas ===")
      for i,item in enumerate(data, start=1):
          print(f"\n\nSeccion {i}")
          print(f"\n{item['content'][:50]}...")  # Mostrar solo los primeros 50 caracteres del contenido
      print("\n============================\n")

      return data
    

    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return []

if __name__ == "__main__":
  data = load_data()
  if data:
      print(f"Total de secciones encontradas: {len(data)}")
  else:
      print("No se encontraron secciones en el PDF.")