# --- Fungsi Utama Kuis ---
def check_guess_options():
    score = 0

    print("--- Selamat Datang di Kuis Matematika Interaktif! ---")
    print("Jawablah pertanyaan berikut dengan mengetik A, B, C, atau D.\n")

    # Loop untuk setiap pertanyaan dalam list
    for i, soal in enumerate(bank_soal):
        print(f"Pertanyaan #{i+1}: {soal['question']}")

        # Mengacak urutan pilihan jawaban
        option_labels = ["A", "B", "C", "D"]

        for j, option in enumerate(soal['options']):
            print(f"  {option_labels[j]}. {option}")

        # Meminta input dari pengguna
        while True:
            user_answer_label = input("Jawabanmu: ").upper()
            if user_answer_label in option_labels:
                # Mencari tahu teks jawaban yang dipilih pengguna
                index = option_labels.index(user_answer_label)
                user_answer_text = soal['options'][index]
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan A, B, C, atau D.")

        # Memeriksa jawaban
        if user_answer_text == soal['answer']:
            print("Benar! ✅\n")
            score += 1
        else:
            print(f"Salah! ❌ Jawaban yang benar adalah {soal['answer']}.\n")

    # Menampilkan hasil akhir
    print("--- Kuis Selesai ---")
    print(f"Skor akhir kamu adalah: {score} dari {len(bank_soal)} pertanyaan.")


# --- Kumpulan Pertanyaan ---
# Kita gunakan list of dictionary untuk menyimpan setiap pertanyaan.
# Setiap dictionary berisi: pertanyaan, pilihan jawaban, dan jawaban yang benar.
bank_soal = [
    {
        "question": "Berapa hasil dari 125 + 25 x 2?",
        "options": ["300", "175", "275", "152"],
        "answer": "175"
    },
    {
        "question": "Berapa hasil dari (200 - 50) : 5?",
        "options": ["30", "40", "50", "150"],
        "answer": "30"
    },
    {
        "question": "Berapa hasil dari 10 x 10 - 10?",
        "options": ["0", "90", "100", "110"],
        "answer": "90"
    },
    {
        "question": "Berapa hasil dari 75 + 100 : 25?",
        "options": ["7", "79", "85", "175"],
        "answer": "79"
    },
    {
        "question": "Berapa hasil dari 9 x (10 + 5)?",
        "options": ["95", "105", "135", "90"],
        "answer": "135"
    },
    {
        "question": "Ani membeli 5 pensil seharga Rp2.000 per buah. Jika dia membayar dengan uang Rp20.000, berapa kembaliannya?",
        "options": ["Rp5.000", "Rp10.000", "Rp12.000", "Rp15.000"],
        "answer": "Rp10.000"
    },
    {
        "question": "Berapa hasil dari 500 : 10 x 2?",
        "options": ["25", "50", "100", "52"],
        "answer": "100"
    },
    {
        "question": "Jika suhu awal adalah 25 derajat Celcius, lalu turun 8 derajat. Berapa suhu sekarang?",
        "options": ["17", "33", "20", "15"],
        "answer": "17"
    }
]

# --- Menjalankan Kuis ---
check_guess_options()