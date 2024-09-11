import random

def generate_code(length):
    """Generuje náhodný kód jako seznam čísel s danou délkou."""
    return [random.randint(0, 9) for _ in range(length)]

def print_code(code):
    """Tiskne kód v přehledném formátu."""
    print("Kód je: " + ''.join(map(str, code)))

def check_combination(code, guess):
    """Zkontroluje, zda je hádaný kód správný."""
    return code == guess

def give_hint(code, guess):
    """Poskytuje nápovědu: Počet čísel na správné pozici a počet správných čísel na špatné pozici."""
    correct_position = 0
    correct_number = 0
    code_copy = code.copy()
    guess_copy = guess.copy()
    
    # Kontrola čísel na správné pozici
    for i in range(len(code)):
        if guess[i] == code[i]:
            correct_position += 1
            code_copy[i] = guess_copy[i] = None  # Označit jako zkontrolované

    # Kontrola správných čísel na špatné pozici
    for i in range(len(guess)):
        if guess_copy[i] is not None and guess_copy[i] in code_copy:
            correct_number += 1
            code_copy[code_copy.index(guess_copy[i])] = None  # Označit číslo jako použité

    return correct_position, correct_number

def get_difficulty():
    """Vrátí úroveň obtížnosti na základě vstupu uživatele."""
    while True:
        print("\nVyberte úroveň obtížnosti:")
        print("1. Snadná (3 čísla, 10 pokusů)")
        print("2. Střední (4 čísla, 8 pokusů)")
        print("3. Těžká (5 čísla, 6 pokusů)")
        
        choice = input("Zadejte číslo úrovně obtížnosti: ")
        if choice == '1':
            return 3, 10
        elif choice == '2':
            return 4, 8
        elif choice == '3':
            return 5, 6
        else:
            print("Neplatná volba. Zvolte 1, 2 nebo 3.")

def main():
    print("Vítejte v dešifrovací hře s nápovědami!")
    
    length, max_attempts = get_difficulty()
    print(f"Vytvořím náhodný kód složený z {length} čísel.")
    
    # Generování náhodného kódu
    code = generate_code(length)
    
    attempts = 0
    
    while attempts < max_attempts:
        try:
            guess = input(f"Zadejte {length}-místnou kombinaci (čísla mezi 0 a 9): ")
            guess = [int(digit) for digit in guess]
            
            if len(guess) != length or any(d < 0 or d > 9 for d in guess):
                print(f"Neplatný vstup. Ujistěte se, že zadáte {length} čísla mezi 0 a 9.")
                continue
            
            if check_combination(code, guess):
                print(f"Gratulujeme! Uhodli jste kód: {code}")
                break
            else:
                # Poskytnout nápovědu
                correct_position, correct_number = give_hint(code, guess)
                print(f"Nápověda: {correct_position} čísla jsou na správné pozici.")
                print(f"Nápověda: {correct_number} správná čísla, ale na špatné pozici.")
            
            attempts += 1
            remaining_attempts = max_attempts - attempts
            print(f"Zbývá pokusů: {remaining_attempts}")
        
        except ValueError:
            print("Neplatný vstup. Ujistěte se, že zadáte čísla.")
    
    if attempts == max_attempts:
        print(f"Prohráli jste. Správný kód byl: {code}")

if __name__ == "__main__":
    main()
