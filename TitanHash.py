import hashlib
import time
import os
import sys
import threading
import queue

def hasher_worker(hasher, q):
    """Worker in background che aggiorna un singolo hash."""
    while True:
        chunk = q.get()
        if chunk is None:  # Segnale di terminazione
            break
        hasher.update(chunk)
        q.task_done()

def calculate_hashes_fast(file_path: str, chunk_size: int = 8 * 1024 * 1024):
    """
    Calcola MD5, SHA-1 e SHA-256 in parallelo usando il multi-threading.
    Massimizza l'uso della CPU e minimizza il collo di bottiglia del disco.
    """
    if not os.path.exists(file_path):
        print(f"Errore: Il file '{file_path}' non esiste.")
        return

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"Analisi del file: {os.path.basename(file_path)}")
    print(f"Dimensione: {file_size_mb:.2f} MB")
    print("Calcolo in corso (Multi-Threading attivato)...")
    
    start_time = time.time()
    
    md5_hasher = hashlib.md5()
    sha1_hasher = hashlib.sha1()
    sha256_hasher = hashlib.sha256()
    
    # Code limitate a 4 blocchi (32MB) per non intasare la RAM se il disco è più veloce della CPU
    q_md5 = queue.Queue(maxsize=4)
    q_sha1 = queue.Queue(maxsize=4)
    q_sha256 = queue.Queue(maxsize=4)
    
    # Creiamo i 3 thread indipendenti (uno per ogni calcolo crittografico)
    t1 = threading.Thread(target=hasher_worker, args=(md5_hasher, q_md5))
    t2 = threading.Thread(target=hasher_worker, args=(sha1_hasher, q_sha1))
    t3 = threading.Thread(target=hasher_worker, args=(sha256_hasher, q_sha256))
    
    t1.start()
    t2.start()
    t3.start()
    
    try:
        total_bytes = os.path.getsize(file_path)
        bytes_read = 0
        last_print_time = time.time()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                # Passa la "referenza" in memoria del blocco ai 3 processori senza copiare dati
                q_md5.put(chunk)
                q_sha1.put(chunk)
                q_sha256.put(chunk)
                
                bytes_read += len(chunk)
                current_time = time.time()
                
                # Barra di caricamento sincronizzata con la lettura dal disco
                if current_time - last_print_time > 0.2:
                    percent = (bytes_read / total_bytes) * 100
                    sys.stdout.write(f"\rLettura Disco: {percent:.1f}% ({bytes_read // (1024*1024)} / {total_bytes // (1024*1024)} MB)")
                    sys.stdout.flush()
                    last_print_time = current_time
                    
        sys.stdout.write(f"\rLettura Disco: 100.0% ({total_bytes // (1024*1024)} / {total_bytes // (1024*1024)} MB)\n")
        sys.stdout.write("Sincronizzazione finale dei calcoli in corso...\r")
        sys.stdout.flush()
        
    except PermissionError:
        print(f"Errore: Nessun permesso per leggere il file '{file_path}'.")
        for q in (q_md5, q_sha1, q_sha256): q.put(None)
        return
    except Exception as e:
        print(f"Errore durante la lettura: {e}")
        for q in (q_md5, q_sha1, q_sha256): q.put(None)
        return

    # Inviamo il comando "Null" per dire ai thread che il file è finito e possono spegnersi
    q_md5.put(None)
    q_sha1.put(None)
    q_sha256.put(None)
    
    # Attendiamo che i 3 thread abbiano digerito gli ultimissimi blocchi in coda
    t1.join()
    t2.join()
    t3.join()
            
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Risultati finali
    md5_result = md5_hasher.hexdigest()
    sha1_result = sha1_hasher.hexdigest()
    sha256_result = sha256_hasher.hexdigest()
    
    # Pulisce la riga precedente
    sys.stdout.write("\033[K")
    print("\n" + "-" * 64)
    print(f"MD5:     {md5_result}")
    print(f"SHA-1:   {sha1_result}")
    print(f"SHA-256: {sha256_result}")
    print("-" * 64)
    
    speed_mb_s = file_size_mb / elapsed_time if elapsed_time > 0 else 0
    print(f"\nTempo totale: {elapsed_time:.3f} secondi")
    print(f"Velocità effettiva: {speed_mb_s:.2f} MB/s")

if __name__ == "__main__":
    print("=== STRUMENTO DI HASH RAPIDO (Multi-Core: MD5, SHA-1, SHA-256) ===")
    
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        calculate_hashes_fast(target_file)
    else:
        print("\nNessun file rilevato!")
        print("ISTRUZIONI: Trascinare un file sopra l'icona di questo script (.py)")
        print("oppure incollare il percorso completo del file qui sotto.")
        print("(Premi INVIO a vuoto per uscire)")
        
        target_file = input("\nPercorso del file: ").strip()
        target_file = target_file.strip('\"').strip('\'')
        
        if target_file:
            calculate_hashes_fast(target_file)
            
    print("\n")
    input("Premi INVIO per chiudere questa finestra...")
