## Menentukan Pertanyaan Bisnis

    1. Bagaimana rata-rata perbulan dari kadar PM2.5 di masing-masing kota?
    2. Bagaimana rata-rata perbulan dari kadar PM10 di masing-masing kota?
    3. Kota mana yang memiliki kondisi kualitas udara yang paling buruk?
    4. Bagaimana pengaruh arah angin dengan kadar PM2.5 di awal tahun 2017 di kota Wanshouxigong?
    5. Rata-rata kadar PM2.5 paling tinggi terjadi di hari apa di setiap kota?
    6. Bagaimana cara mengurangi kadar PM2.5 pada udara?

## Cara Menjalankan Program Streamlit

Buatlah pada environment baru untuk streamlit, ikuti langkah-langkah di bawah ini :

Pertama, jalankan kode ini

    conda create -n streamlit-env
    conda activate streamlit-env

Setelah itu, install semua package/module yang digunakan pada file requirements.txt

    pip install -r requirements.txt

Masukkan directory tempat menyimpan file app.py

    cd [directory]

Jalankan file app.py

    streamlit run app.py
