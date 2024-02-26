import subprocess
import argparse

def run_script(script_name, args=None):
    """Esegue uno script Python con gli argomenti specificati e attende che termini."""
    if args is None:
        args = []
    command = ["python", script_name] + args
    print(f"Esecuzione di {script_name} con parametri {args}...")
    subprocess.run(command, check=True)
    print(f"{script_name} completato.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("param1", help="Descrizione del Parametro 1 per script1 e script2")
    parser.add_argument("param2", help="Descrizione del Parametro 2 per script1 e script2")
    args = parser.parse_args()

    # Esegue gli script in sequenza passando i parametri necessari
    run_script("script1.py", [args.param1, args.param2])
    run_script("script2.py", [args.param1, args.param2])
    run_script("script3.py")  # Assumendo che script3 non richieda parametri

if __name__ == "__main__":
    main()
