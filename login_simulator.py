import time
import random
import sys
from collections import deque
from datetime import datetime
from colorama import init, Fore, Style

# Inisialisasi colorama
init(autoreset=True)

# USER DATA DEFAULT (untuk demo)
USERS = {
    "admin": "Passw0rd!",
    "guest": "guest1234",
    "user1": "welcome2025"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Linux; Android 10; Mobile)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

MAX_ATTEMPTS = 5
TIME_WINDOW = 60
LOCKOUT_BASE = 5  # dari 30 jadi 5 detik dasar

LOG_FILE = "bruteforce_sim_log.txt"

def log_attempt(username, password, success, user_agent):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAIL"
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | {username}:{password} | {status} | UA: {user_agent}\n")

def progress_bar(progress, total):
    percent = int(progress / total * 100)
    bar = ('#' * int(percent / 4)).ljust(25)
    sys.stdout.write(f"\r[{bar}] {percent}% ")
    sys.stdout.flush()

class RateLimiter:
    def __init__(self):
        self.attempt_times = deque()
        self.locked_until = 0
        self.lockout_duration = LOCKOUT_BASE
        self.fail_streak = 0

    def can_attempt(self):
        now = time.time()
        if now < self.locked_until:
            return False, int(self.locked_until - now)
        while self.attempt_times and now - self.attempt_times[0] > TIME_WINDOW:
            self.attempt_times.popleft()
        if len(self.attempt_times) < MAX_ATTEMPTS:
            return True, 0
        else:
            backoff = min(self.lockout_duration * (2 ** self.fail_streak), 60)
            self.locked_until = now + backoff
            return False, int(backoff)

    def add_attempt(self, success):
        self.attempt_times.append(time.time())
        if success:
            self.fail_streak = 0
        else:
            self.fail_streak += 1

def captcha_challenge():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    print(Fore.MAGENTA + f"Captcha Challenge: What is {a} + {b}?")
    try:
        ans = int(input("Answer: "))
        return ans == a + b
    except:
        return False

def animate_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def colored_on_off(flag):
    return Fore.RED + "ON 🔴" if flag else Fore.GREEN + "OFF 🟢"

def toggle_animation(feature_name, status):
    animate_text(Fore.YELLOW + f"Toggling {feature_name} to {'ON 🔴' if status else 'OFF 🟢'}", 0.05)
    for _ in range(3):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.3)
    print("\n")

def print_menu(use_captcha, use_progress, use_user_agent, use_delay):
    print(Fore.CYAN + Style.BRIGHT + "╔" + "═"*48 + "╗")
    print(Fore.CYAN + Style.BRIGHT + "║" + " "*15 + "🔐 Brute Force Simulator 🔐" + " "*15 + "║")
    print(Fore.CYAN + Style.BRIGHT + "╠" + "═"*48 + "╣")

    print(Fore.YELLOW + " 1. 📝 Manual Login")
    print(Fore.YELLOW + " 2. 🚀 Brute Force Otomatis (wordlist)")
    print(Fore.MAGENTA + f" 3. 🛡 Toggle Captcha           : {colored_on_off(use_captcha)}")
    print(Fore.MAGENTA + f" 4. 📊 Toggle Progress & Stats : {colored_on_off(use_progress)}")
    print(Fore.MAGENTA + f" 5. 🌐 Toggle User-Agent Sim   : {colored_on_off(use_user_agent)}")
    print(Fore.MAGENTA + f" 6. ⏱ Toggle Auto Delay        : {colored_on_off(use_delay)}")
    print(Fore.CYAN + " 7. 🎯 Mode Challenge (Random User/Pass)")
    print(Fore.RED + " 8. ❌ Keluar")
    print(Fore.CYAN + "╚" + "═"*48 + "╝")

def manual_login(rate_limiter, use_captcha, use_user_agent):
    print("\n=== Manual Login ===")
    while True:
        can_try, wait = rate_limiter.can_attempt()
        if not can_try:
            print(Fore.RED + f"[!] Rate limited. Please wait {wait} seconds.")
            time.sleep(wait)
            continue

        username = input("Username: ").strip()
        password = input("Password: ").strip()
        ua = random.choice(USER_AGENTS) if use_user_agent else "N/A"

        if use_captcha and rate_limiter.fail_streak >= 3:
            if not captcha_challenge():
                print(Fore.RED + "[!] Captcha failed! Try again.")
                continue

        success = USERS.get(username) == password
        rate_limiter.add_attempt(success)
        log_attempt(username, password, success, ua)

        if success:
            print(Fore.GREEN + "[+] Login SUCCESS!")
            break
        else:
            print(Fore.RED + "[-] Login FAILED!")

def brute_force(rate_limiter, user_list, pass_list, use_captcha, use_user_agent, use_progress, use_delay):
    print("\n=== Starting Brute Force Attack ===")
    total_attempts = len(user_list) * len(pass_list)
    attempt_count = 0
    success_found = False
    for username in user_list:
        for password in pass_list:
            can_try, wait = rate_limiter.can_attempt()
            if not can_try:
                print(Fore.RED + f"\n[!] Rate limited. Waiting {wait} seconds...")
                time.sleep(wait)
            ua = random.choice(USER_AGENTS) if use_user_agent else "N/A"

            if use_captcha and rate_limiter.fail_streak >= 3:
                if not captcha_challenge():
                    print(Fore.RED + "[!] Captcha failed! Skipping this attempt.")
                    rate_limiter.add_attempt(False)
                    continue

            print(f"Trying {username}:{password} [UA: {ua}] ...", end='')
            attempt_count += 1
            success = USERS.get(username) == password
            rate_limiter.add_attempt(success)
            log_attempt(username, password, success, ua)

            if use_progress:
                progress_bar(attempt_count, total_attempts)

            if use_delay:
                time.sleep(random.uniform(0.1, 0.4))
            else:
                time.sleep(0.1)

            if success:
                print(Fore.GREEN + " SUCCESS!")
                success_found = True
                break
            else:
                print(Fore.RED + " FAIL")
        if success_found:
            break
    if not success_found:
        print(Fore.RED + "\n[-] Password not found.")

def mode_challenge(rate_limiter, use_captcha, use_user_agent):
    print("\n=== Mode Challenge ===")
    rand_user = "user" + str(random.randint(1000, 9999))
    rand_pass = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%", k=8))
    USERS[rand_user] = rand_pass
    print(Fore.YELLOW + f"[!] New user created: {rand_user} with unknown password. Try to find it by brute force!")
    print(Fore.YELLOW + "Use manual login atau brute force dengan wordlist.")

def main():
    rate_limiter = RateLimiter()
    use_captcha = False
    use_progress = True
    use_user_agent = True
    use_delay = True

    while True:
        print_menu(use_captcha, use_progress, use_user_agent, use_delay)
        choice = input(Fore.WHITE + Style.BRIGHT + "\nPilih menu (1-8): ").strip()

        if choice == "1":
            manual_login(rate_limiter, use_captcha, use_user_agent)
        elif choice == "2":
            user_list = list(USERS.keys())
            pass_list = ["123456", "password", "Passw0rd!", "welcome2025", "guest1234", "admin123"]
            brute_force(rate_limiter, user_list, pass_list, use_captcha, use_user_agent, use_progress, use_delay)
        elif choice == "3":
            use_captcha = not use_captcha
            toggle_animation("Captcha", use_captcha)
        elif choice == "4":
            use_progress = not use_progress
            toggle_animation("Progress Bar & Statistik", use_progress)
        elif choice == "5":
            use_user_agent = not use_user_agent
            toggle_animation("User-Agent Simulation", use_user_agent)
        elif choice == "6":
            use_delay = not use_delay
            toggle_animation("Auto Delay", use_delay)
        elif choice == "7":
            mode_challenge(rate_limiter, use_captcha, use_user_agent)
        elif choice == "8":
            print(Fore.RED + Style.BRIGHT + "Terima kasih sudah menggunakan program ini. 🙏")
            break
        else:
            print(Fore.RED + "[!] Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()
