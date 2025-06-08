<!DOCTYPE html>
<html lang="es">
<head>
  <h1>Sistema de Conteo de Objetos por Zona de Ingreso</h1>

  <p>
    Este proyecto implementa un sistema de visión por computadora que detecta y cuenta objetos de color azul que ingresan por primera vez a una zona definida en el centro de la imagen. Utiliza OpenCV para la detección de color, procesamiento de contornos y seguimiento básico entre fotogramas. Este sistema es una base ideal para aplicaciones de conteo de personas, seguimiento de entrada/salida o control de zonas en sistemas automatizados.
  </p>

  <h2>Funcionamiento General</h2>
  <ul>
    <li>Se captura video desde la cámara web.</li>
    <li>Se define una zona de conteo en forma de rectángulo rojo.</li>
    <li>El sistema detecta objetos azules usando máscaras HSV.</li>
    <li>Se calcula el centroide de cada objeto detectado.</li>
    <li>Si un objeto entra por primera vez a la zona, se incrementa el contador y se marca su centroide con un punto verde.</li>
    <li>El sistema evita contar el mismo objeto múltiples veces mientras permanezca dentro de la zona.</li>
  </ul>

  <h2>Muestra de Funcionamiento</h2>
  <p>A continuación se muestra un ejemplo de cómo funciona el sistema. Cuando un objeto azul entra por primera vez a la zona roja, el conteo aumenta:</p>

  <div class="image">
    <!-- Reemplaza este src con tu imagen o GIF -->
    <img src="demo.gif" alt="Demostración del sistema en funcionamiento" width="500">
  </div>
</body>
</html>

