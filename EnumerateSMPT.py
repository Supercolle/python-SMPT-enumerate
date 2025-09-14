import telnetlib
import time

def connect_smtp(host, port):
    tn = telnetlib.Telnet(host, port, timeout=10)
    banner = tn.read_until(b"\n").decode(errors="ignore").strip()
    print(f"[+] Connesso: {banner}")
    return tn

def vrfy_users(host, port):
    users = [
        "michael","james","john","robert","david","william","mary",
        "christopher","joseph","richard","daniel","thomas","matthew",
        "jennifer","charles","anthony","patricia","linda","mark",
        "elizabeth","joshua","steven","andrew","kevin","brian","barbara",
        "jessica","jason","susan","timothy","paul","kenneth","lisa",
        "ryan","sarah","karen","jeffrey","donald","ashley","eric",
        "jacob","nicholas","jonathan","ronald","michelle","kimberly",
        "nancy","justin","sandra","amanda","brandon","stephanie","emily",
        "melissa","gary","edward","stephen","scott","george","donna",
        "jose","rebecca","deborah","laura","cynthia","carol","amy",
        "margaret","gregory","sharon","larry","angela","maria","alexander",
        "benjamin","nicole","kathleen","patrick","samantha","tyler",
        "samuel","betty","brenda","pamela","aaron","kelly","robin",
        "heather","rachel","adam","christine","zachary","debra","katherine",
        "dennis","nathan","christina","julie","jordan","kyle","anna"
    ] #change whit ur own user list if needed

    results = []

    tn = connect_smtp(host, port)

    for user in users:
        try:
            tn.write(f"VRFY {user}\r\n".encode())
            resp = tn.read_until(b"\n", timeout=3).decode(errors="ignore").strip()
            print(f"[{user}] -> {resp}")

            if resp.startswith("250"):
                results.append(user)

            elif resp.startswith("421"):
                # Server ha chiuso la connessione, riconnetto
                print("[!] Connessione chiusa dal server, riconnessione...")
                tn.close()
                time.sleep(2)
                tn = connect_smtp(host, port)

        except Exception as e:
            print(f"[!] Errore su {user}: {e}")
            try:
                tn.close()
            except:
                pass
            tn = connect_smtp(host, port)

    tn.write(b"QUIT\r\n")
    tn.close()

    print("\n=== Utenti trovati ===")
    for u in results:
        print(u)

if __name__ == "__main__":
    host = "targetip"#change this with your target IP
    port = 25
    vrfy_users(host, port)
