<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Image → ASCII | Hugo François</title>
  <meta name="description" content="Convertisseur d’images en art ASCII avec Pyodide.">
  <link rel="stylesheet" href="../style.css" />
  <style>
    #ascii-output {
      background: #000;
      color: #0f0;
      font-family: monospace;
      white-space: pre;
      padding: 10px;
      border-radius: 8px;
      overflow-x: auto;
      max-height: 600px;
      font-size: 10px;
      line-height: 8px;
    }
    input[type="file"] {
      margin: 12px 0;
    }
  </style>
</head>
<body>
  <canvas id="canvas"></canvas><canvas id="canvas2"></canvas>

  <header class="site-header">
    <div class="container header-inner">
      <h1>Image → ASCII</h1>
      <p class="subtitle">Convertisseur d’images en art ASCII interactif</p>
    </div>
  </header>

  <main class="container section">
    <h2>Présentation</h2>
    <p>
      Ce projet convertit des images en art ASCII en mappant chaque pixel sur un caractère selon sa luminosité.  
      Le code d’origine a été adapté ici pour s’exécuter directement dans le navigateur via <strong>Pyodide</strong>.
    </p>

    <h2>Exemples</h2>

    <figure class="project-media">
      <img src="../assets/images/ascii_usa_img.png" alt="Image originale" />
      <figcaption>Image originale utilisée pour la démonstration.</figcaption>
    </figure>

    <figure class="project-media">
      <img src="../assets/images/ascii_usa.png" alt="Résultat ASCII" />
      <figcaption>Résultat généré (image convertie en ASCII).</figcaption>
    </figure>

    <h2>Tester le convertisseur</h2>
    <p>Chargez votre propre image pour la transformer en art ASCII :</p>

    <input type="file" id="imageInput" accept="image/*" />
    <pre id="ascii-output">⏳ En attente d’image...</pre>

    <div style="margin-top:30px;">
      <a href="../index.html#projects" class="btn ghost">← Retour au portfolio</a>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© 2025 Hugo François — Projet Image → ASCII</p>
    </div>
  </footer>

  <!-- Pyodide -->
  <script src="https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js"></script>
  <script>
    async function main() {
      const pyodide = await loadPyodide();
      await pyodide.loadPackage("pillow");

      // Code Python chargé dans Pyodide
      const pythonCode = `
from PIL import Image
import io

ASCII_CHARS = "Ñ@#W$9876543210?!abc;:+=-,._' "

def image_to_ascii(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("L")
    width, height = img.size
    new_width = 100
    new_height = int((height / width) * new_width * 0.55)
    img = img.resize((new_width, new_height))
    pixels = img.getdata()
    ascii_str = ''.join(ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels)
    ascii_img = '\\n'.join(ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width))
    return ascii_img
      `;
      await pyodide.runPythonAsync(pythonCode);

      // Gestion du fichier uploadé
      const input = document.getElementById("imageInput");
      const output = document.getElementById("ascii-output");

      input.addEventListener("change", async () => {
        const file = input.files[0];
        if (!file) return;
        output.textContent = "⏳ Conversion en cours...";
        try {
          const buffer = await file.arrayBuffer();
          const uint8 = new Uint8Array(buffer);
          pyodide.globals.set("image_bytes", uint8);
          const result = await pyodide.runPythonAsync("image_to_ascii(image_bytes)");
          output.textContent = result;
        } catch (err) {
          output.textContent = "❌ Erreur : " + err.message;
        }
      });
    }

    main();
  </script>

  <script src="../background.js"></script>
</body>
</html>
