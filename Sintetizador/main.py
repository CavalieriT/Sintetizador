"""
Sintetizador Didáctico - Punto de entrada principal
Aplicación educativa para aprender síntesis de audio básica.

Uso:
    py main.py          (recomendado en Windows)
    python main.py      (si Python está en el PATH)
"""

import sys
import os

def verificar_dependencias():
    """Verifica que todas las dependencias necesarias estén instaladas."""
    dependencias_requeridas = {
        'tkinter': 'tkinter (incluido con Python)',
        'numpy': 'numpy',
        'sounddevice': 'sounddevice',
        'matplotlib': 'matplotlib'
    }
    
    faltantes = []
    
    for modulo, nombre_display in dependencias_requeridas.items():
        try:
            __import__(modulo)
        except ImportError:
            faltantes.append((modulo, nombre_display))
    
    if faltantes:
        print("=" * 75)
        print(" ERROR: Faltan dependencias necesarias")
        print("=" * 75)
        print("\nPaquetes faltantes:")
        for modulo, display in faltantes:
            print(f"  • {display}")
        
        # Mostrar comando de instalación
        paquetes_pip = ' '.join([m for m, _ in faltantes if m != 'tkinter'])
        if paquetes_pip:
            print("\nPara instalarlos, ejecuta:")
            print(f"\n  py -m pip install {paquetes_pip}")
            print(f"\n  O alternativamente:")
            print(f"  python -m pip install {paquetes_pip}")
        
        if any(m == 'tkinter' for m, _ in faltantes):
            print("\n⚠️  NOTA IMPORTANTE:")
            print("  tkinter viene incluido con Python.")
            print("  Si falta, reinstala Python desde: https://www.python.org")
            print("  Marca la opción 'Add Python to PATH' durante la instalación.")
        
        print("=" * 75)
        sys.exit(1)

def main():
    """Función principal que inicializa y ejecuta la aplicación."""
    print("=" * 75)
    print(" SINTETIZADOR DIDÁCTICO")
    print(" Aplicación educativa para síntesis de audio")
    print("=" * 75)
    print("\nVerificando dependencias...", end=" ", flush=True)
    
    # Verificar dependencias
    verificar_dependencias()
    print("✓ OK\n")
    
    try:
        # Importar la clase principal
        print("Cargando módulos...", end=" ", flush=True)
        from ui.interfaz import SintetizadorApp
        print("✓ OK\n")
        
        # Iniciar aplicación
        print("Iniciando interfaz gráfica...")
        print("=" * 75)
        app = SintetizadorApp()
        app.mainloop()
        
    except ImportError as e:
        print("\n" + "=" * 75)
        print(" ERROR: No se pudo importar un módulo")
        print("=" * 75)
        print(f"\nDetalles: {e}")
        print(f"\nUbicación actual: {os.getcwd()}")
        print(f"Ubicación esperada: ...\\TFG\\Sintetizador")
        print("\nVerifica que estés en la carpeta raíz del proyecto.")
        print("Si no lo estás, ejecuta:")
        print("  cd C:\\TFG\\Sintetizador")
        print("  py main.py")
        print("=" * 75)
        sys.exit(1)
        
    except Exception as e:
        print("\n" + "=" * 75)
        print(" ERROR INESPERADO")
        print("=" * 75)
        print(f"\nTipo de error: {type(e).__name__}")
        print(f"Mensaje: {e}\n")
        
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 75)
        print("Si el problema persiste, verifica:")
        print("  1. Que todas las dependencias estén instaladas")
        print("  2. Que los archivos del proyecto estén completos")
        print("  3. Que no haya errores de sintaxis en el código")
        print("=" * 75)
        sys.exit(1)

if __name__ == "__main__":
    main()