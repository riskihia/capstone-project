GetAuthExample = {
    "data": {
        "email": "user5@example.com",
        "id": "daaa2c25-3550-47fa-869d-f5bcc0b5e675",
        "photo": None,
        "premium": False,
        "terakhir_login": "Wed, 31 May 2023 07:26:54 GMT",
        "token": "ukDFYsC50YUX0g",
        "username": "user5",
    },
    "error": False,
    "message": "User successfully registered",
}

GetLahanExample = {
    "data": [
        {
            "id": "lahan1",
            "nama": "Lahan 1",
            "image": "https://example.com/lahan1.jpg",
            "luas": 10.5,
            "alamat": "Jl. Lahan 1, Bandung",
            "lat": -6.917464,
            "lon": 107.619123,
        },
        {
            "id": "lahan2",
            "nama": "Lahan 2",
            "image": "https://example.com/lahan2.jpg",
            "luas": 20.0,
            "alamat": "Jl. Lahan 2, Jakarta",
            "lat": -6.200000,
            "lon": 106.816666,
        },
    ],
    "error": False,
    "message": "User successfully registered",
}

PostLahanExample = {"error": False, "message": "Lahan added successfully"}
DeleteLahanExample = {"error": False, "message": "Lahan deleted successfully"}
GetLahanIdExample = {
    "error": "boolean",
    "message": "string",
    "data": {
        "id": "string",
        "nama": "string",
        "image": "string",
        "luas": "double",
        "alamat": "string",
        "lat": "double",
        "lon": "double",
        "tanam": {
            "id": "string",
            "jarak": "integer",
            "status": "enum",
            "tanggal_tanam": "date",
            "tanggal_panen": "date",
            "jumlah_panen": "integer",
            "harga_panen": "integer",
            "umur": "integer",
            "bibit": {
                "id": "string",
                "nama": "string",
                "photo": "string",
                "deskripsi": "text",
                "harga_beli": "integer",
                "jenis": "enum",
                "link_market": "string",
            },
            "aktivitas": [
                {
                    "id": "string",
                    "nama": "string",
                    "keterangan": "text",
                    "pupuk": "integer",
                    "tanggal_aktifitas": "date",
                },
            ],
        },
    },
}


LogoutAuthExample = {"error": False, "message": "User successfully logged out"}

UserAuthExample = {
    "error": False,
    "message": "User data fetched successfully",
    "data": {
        "id": "abcd1234",
        "username": "user1",
        "email": "user1@example.com",
        "photo": "https://example.com/photo.jpg",
        "premium": False,
        "lasted_login": "2023-05-23T10:00:00Z",
        "lahan": [
            {
                "id": "ABC",
                "nama": "Lahan 1",
                "image": "url_image.png",
                "luas": 8,
                "alamat": "Alamat Lengkap",
                "lat": None,
                "lon": None,
            }
        ],
    },
}

GetLahanAuthExample = {
    "error": False,
    "message": "All lahan data fetched successfully",
    "data": [
        {
            "id": "lahan1",
            "nama": "Lahan 1",
            "image": "https://example.com/lahan1.jpg",
            "luas": 10.5,
            "alamat": "Jl. Lahan 1, Bandung",
            "lat": -6.917464,
            "lon": 107.619123,
        },
        {
            "id": "lahan2",
            "nama": "Lahan 2",
            "image": "https://example.com/lahan2.jpg",
            "luas": 20.0,
            "alamat": "Jl. Lahan 2, Jakarta",
            "lat": -6.200000,
            "lon": 106.816666,
        },
    ],
}

AddLahanAuthExample = {"error": False, "message": "Lahan added successfully"}

DeleteLahanAuthExample = {"error": False, "message": "Lahan deleted successfully"}

DetailLahanAuthExample = {
    "error": False,
    "message": "Detail lahan fetched successfully",
    "data": {
        "id": "lahan1",
        "nama": "Lahan 1",
        "image": "https://example.com/lahan1.jpg",
        "luas": 10.5,
        "alamat": "Jl. Lahan 1, Bandung",
        "lat": -6.917464,
        "lon": 107.619123,
        "tanam": {
            "id": "tanam1",
            "jarak": 30,
            "status": "plan",
            "tanggal_tanam": "2023-06-04",
            "tanggal_panen": None,
            "jumlah_panen": None,
            "harga_panen": None,
            "umur": 0,
            "bibit": {
                "id": "bibit1",
                "nama": "Bibit Tomat",
                "photo": "https://example.com/bibit1.jpg",
                "deskripsi": "Bibit tomat unggul",
                "harga_beli": 10000,
                "jenis": "Sayuran",
                "link_market": "https://tani.iyabos.com/marketplace",
            },
            "aktivitas": [
                {
                    "id": "aktivitas1",
                    "nama": "Pemupukan",
                    "keterangan": "Pemupukan tahap 1",
                    "pupuk": 1,
                    "tanggal_aktifitas": "2023-06-04",
                }
            ],
        },
    },
}

GetHasilIot = {"error": False, "message": "Data IoT berhasil ditambahkan"}
PostTanamPlan = {"error": False, "message": "Data plan tanam berhasil ditambahkan"}
PostTanamPlanNotfound = {"error": True, "message": "Bibit atau lahan tidak ditemukan"}
PostTanamPlanAlready = {
    "error": True,
    "message": "Lahan sudah mempunyai rencana atau proses tanam",
}
DeleteTanam = {"error": False, "message": "Data tanam berhasil dihapus"}
DeleteTanamNotfound = {
    "error": True,
    "message": "Data tanam tidak ditemukan atau sudah dihapus",
}
PostTanamExec = {
    "error": False,
    "message": "Status tanam berhasil diubah menjadi 'exec'",
}
PostTanamExecNotfound = {
    "error": True,
    "message": "Data tanam tidak ditemukan atau status bukan 'plan'",
}

GetTanamClose = {
    "error": False,
    "message": "Data tanam berhasil diambil",
    "data": [
        {
            "id": "tanam1",
            "bibit_nama": "bibit1",
            "jarak": 30,
            "status": "close",
            "tanggal_tanam": "2023-06-12",
            "tanggal_panen": "2023-07-15",
            "jumlah_panen": 500,
            "harga_panen": 10000,
        }
    ],
}

GetTanamCloseNotfound = {"error": True, "message": "Lahan tidak ditemukan"}

PostTanamClose = {
    "error": False,
    "message": "Status tanam berhasil diubah menjadi 'close'",
}
PostTanamCloseNotfound = {
    "error": True,
    "message": "Data tanam tidak ditemukan atau status bukan 'exec'",
}

PostTanamRekomendasi = {
    "error": False,
    "message": "Berhasil mendapatkan rekomendasi bibit",
    "data": {
        "bibit": [
            {
                "id": "bibit123",
                "nama": "Bibit Tomat",
                "photo": "url",
                "deskripsi": "Deskripsi bibit",
                "harga_beli": 10000,
                "jenis": "Sayuran",
                "link_market": "url",
            },
        ]
    },
}

PostTanamRekomendasiNot = {"error": True, "message": "Data tidak valid"}


GetIot = {
    "error": False,
    "message": "Data berhasil didapat",
    "data": {"suhu": 25.5, "kelembaban_udara": 60.5},
}

PostIot = {"error": False, "message": "IOT berhasil didaftarkan di lahan"}

PostIotNotfound = {"error": True, "message": "IOT atau lahan tidak ditemukan"}
PostIotAlready = {
    "error": True,
    "message": "IOT sudah terdaftar di lahan lain (nama lahan)",
}

PostIotReset = {"error": False, "message": "Pendaftaran IOT berhasil direset"}
PostIotResetNotfound = {
  "error": True,
  "message": "IOT tidak ditemukan"
}


GetIotNotfound = {"error": True, "message": "Data tidak ditemukan"}
PostRekomendasiIot = {
    "error": False,
    "message": "Berhasil mendapatkan rekomendasi bibit",
    "data": {
        "bibit": [
            {
                "id": "bibit123",
                "nama": "Bibit Tomat",
                "photo": "url",
                "deskripsi": "Deskripsi bibit",
                "harga_beli": 10000,
                "jenis": "Sayuran",
                "link_market": "url",
            },
        ]
    },
}

PostRekomendasiIotNotvalid = {"error": True, "message": "Data tidak valid"}

GetBibit = {
    "error": False,
    "message": "Data bibit fetched successfully",
    "data": [
        {
            "id": "bibit1",
            "nama": "Bibit Tomat",
            "photo": "https://example.com/bibit1.jpg",
            "deskripsi": "Bibit tomat unggul",
            "harga_beli": 10000,
            "jenis": "Sayuran",
            "link_market": "https://tani.iyabos.com/marketplace",
        },
    ],
}
