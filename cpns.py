import requests
import json
import xlwt

# Fungsi untuk mengirim request ke API dan mendapatkan data JSON
def get_api_data(api_url, batch_size=10):
    all_data = []
    offset = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://sscasn.bkn.go.id',
        'Accept': 'application/json',
        'Origin': 'https://sscasn.bkn.go.id'
    }
    
    while True:
        try:
            # Modifikasi URL untuk menggunakan parameter offset dengan format string style Python 2.7
            paginated_url = "{}&offset={}".format(api_url, offset)
            response = requests.get(paginated_url, headers=headers)
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                if data['status'] == 200 and not data['error']:
                    # Jika tidak ada data lagi, hentikan loop
                    if not data['data']['data']:
                        break
                    
                    # Tambahkan data dari halaman ini ke daftar all_data
                    all_data.extend(data['data']['data'])
                    
                    # Tingkatkan offset untuk mengambil halaman berikutnya
                    offset += batch_size
                else:
                    print("Status API bukan 200 atau ada error:", data['message'])
                    break
            else:
                print("Gagal mendapatkan data dari API, status code:", response.status_code)
                break
        except Exception as e:
            print("Error:", e)
            break
    
    return all_data

# Fungsi untuk menyimpan data ke dalam file Excel
def save_to_excel(data, filename):
    # Membuat workbook baru dan sheet
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('Data CPNS')

    # Menulis header kolom
    headers = ['Jabatan', 'Instansi', 'Unit Kerja', 'Formasi', 'Jenis Formasi', 'Disabilitas?', 'Gaji Min', 'Gaji Max', 'Jumlah Kebutuhan']
    for col, header in enumerate(headers):
        sheet.write(0, col, header)
    
    # Menulis data ke file Excel
    for row, item in enumerate(data, start=1):
        sheet.write(row, 0, item.get('jabatan_nm', 'N/A'))
        sheet.write(row, 1, item.get('ins_nm', 'N/A'))
        sheet.write(row, 2, item.get('lokasi_nm', 'N/A'))
        sheet.write(row, 3, item.get('jp_nama', 'N/A'))
        sheet.write(row, 4, item.get('formasi_nm', 'N/A'))
        sheet.write(row, 5, item.get('disable', 'N/A'))
        sheet.write(row, 6, item.get('gaji_min', 'N/A'))
        sheet.write(row, 7, item.get('gaji_max', 'N/A'))
        sheet.write(row, 8, item.get('jumlah_formasi', 'N/A'))
    
    # Simpan workbook ke file Excel
    wb.save(filename)
    print("Data berhasil disimpan ke", filename)

# URL API
api_url = "https://api-sscasn.bkn.go.id/2024/portal/spf?kode_ref_pend=5100144&formasi=UMUM"

# Mengambil semua data dari API
data = get_api_data(api_url, batch_size=10)

if data:
    # Simpan semua data ke Excel
    save_to_excel(data, 'cpns_data_sisteminformasi.xls')
else:
    print("Tidak ada data yang ditemukan atau terjadi kesalahan.")