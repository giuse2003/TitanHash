# ⚡ TitanHash

**TitanHash** è uno strumento di calcolo hash ad altissime prestazioni scritto in Python, progettato per sfruttare al 100% l'architettura Multi-Core dei moderni processori ed eliminare i colli di bottiglia solitamente causati dall'I/O del disco.

## 🚀 Caratteristiche
- **Architettura Multi-Core Asincrona:** Sfrutta il Multi-Threading e pattern Producer-Consumer per parallelizzare i calcoli crittografici.
- **Zero Colli di Bottiglia:** Il disco rigido legge i file enormi alla sua massima velocità di targa (in chunk ottimali da 8MB) senza mai doversi fermare ad attendere la fine dei calcoli della CPU.
- **3 Hash in 1 (Senza rallentamenti):** Calcola contemporaneamente **MD5, SHA-1 e SHA-256**. Essendo eseguiti in parallelo su core diversi, l'aggiunta di algoritmi complessi non impatta sul tempo di lettura del disco.
- **Supporto Drag-and-Drop (Windows):** Trascina direttamente file da decine o centinaia di Gigabyte sull'icona dello script per avviare il calcolo immediato.
- **Interfaccia Intelligente:** Barra di progresso super-ottimizzata che si aggiorna in real-time senza inondare la console di stampa, preservando le performance.

## ⚙️ Come si usa
1. Scarica o clona il progetto.
2. Trascina un qualsiasi file di grandi dimensioni sopra l'icona di `TitanHash.py`.
3. In alternativa, puoi lanciare lo script dal terminale o aprirlo con un doppio clic per incollare manualmente il percorso del file.

## 🛠️ Dettagli Tecnici
Implementato interamente in **Python**, il sistema aggira i limiti del Global Interpreter Lock (GIL) delegando le chiamate `hashlib.update` a thread separati. Il consumo di RAM è limitato rigidamente a 32MB massimi, impedendo saturation della memoria se il disco rigido dovesse superare la velocità di calcolo della CPU.
