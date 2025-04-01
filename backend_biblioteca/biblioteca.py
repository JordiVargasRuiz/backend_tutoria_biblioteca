from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/buscar_libros/")
def buscar_libros(query: str):
    try:
        # Usamos la API de búsqueda de Project Gutenberg
        url = f"https://gutendex.com/books/?search={query}"
        response = requests.get(url)
        data = response.json()

        # Verificar si la respuesta contiene datos
        print("Respuesta de la API:", data)

        if 'results' in data:
            libros = []
            for libro in data['results']:
                title = libro.get('title', "").strip()
                authors = libro.get('authors', [])
                author = authors[0].get('name', "Desconocido").strip() if authors else "Desconocido"
                gutenberg_id = libro.get('id', None)
                cover_url = libro.get('formats', {}).get('image/jpeg', None)

                # Información adicional: idioma
                language = libro.get('languages', ['Desconocido'])[0]  # Usamos el primer idioma

                # Depuración: Ver los valores antes de agregarlos
                print(f"Procesando libro: {title} por {author}, Idioma: {language}")


                epub_url = f"https://www.gutenberg.org/ebooks/{gutenberg_id}.epub.noimages" if gutenberg_id else None
                epub_full_url = f"https://www.gutenberg.org/ebooks/{gutenberg_id}.epub" if gutenberg_id else None
                html_url = f"https://www.gutenberg.org/ebooks/{gutenberg_id}.html" if gutenberg_id else None
                mobi_url = f"https://www.gutenberg.org/ebooks/{gutenberg_id}.mobi" if gutenberg_id else None

                # Asegurarse de que title y author son válidos antes de agregar el libro
                if title and (author != "Desconocido"):
                    libro_info = {
                        "title": title,
                        "author": author,
                        "cover_url": cover_url,
                        "language": language,
                        "download_link_epub_noimages": epub_url,
                        "download_link_epub_full": epub_full_url,
                        "download_link_html": html_url,
                        "download_link_mobi": mobi_url,
                    }
                    libros.append(libro_info)

            return {"books": libros}
        else:
            return {"books": []}
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        raise HTTPException(status_code=500, detail="Error interno en el servidor")
