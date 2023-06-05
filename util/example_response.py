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

LogoutAuthExample = {
  "error": "boolean",
  "message": "string"
}

UserAuthExample = {
  "error": false,
  "message": "User data fetched successfully",
  "data": {
    "id": "abcd1234",
    "username": "user1",
    "email": "user1@example.com",
    "photo": "https://example.com/photo.jpg",
    "premium": false,
    "lasted_login": "2023-05-23T10:00:00Z",
    "lahan": [
      {
      "id": "ABC",
      "nama": "Lahan 1",
      "image": "url_image.png",
      "luas": 8,
      "alamat": "Alamat Lengkap",
      "lat": null,
      "lon": null
      }
    ]
  }
}

GetLahanAuthExample = {
  "error": false,
  "message": "All lahan data fetched successfully",
  "data": [
    {
      "id": "lahan1",
      "nama": "Lahan 1",
      "image": "https://example.com/lahan1.jpg",
      "luas": 10.5,
      "alamat": "Jl. Lahan 1, Bandung",
      "lat": -6.917464,
      "lon": 107.619123
    },
    {
      "id": "lahan2",
      "nama": "Lahan 2",
      "image": "https://example.com/lahan2.jpg",
      "luas": 20.0,
      "alamat": "Jl. Lahan 2, Jakarta",
      "lat": -6.200000,
      "lon": 106.816666
    },
  ]
}

AddLahanAuthExample = {
  "error": false,
  "message": "Lahan added successfully"
}

DeleteLahanAuthExample = {
  "error": false,
  "message": "Lahan deleted successfully"
}

DetailLahanAuthExample = {
  "error": false,
  "message": "Detail lahan fetched successfully",
  "data": {
    "id": "lahan1",
    "nama": "Lahan 1",
    "image": "https://example.com/lahan1.jpg",
    "luas": 10.5,
    "alamat": "Jl. Lahan 1, Bandung",
    "lat": -6.917464

,
    "lon": 107.619123,
    "tanam": {
      "id": "tanam1",
      "jarak": 30,
      "status": "plan",
      "tanggal_tanam": "2023-06-04",
      "tanggal_panen": null,
      "jumlah_panen": null,
      "harga_panen": null,
      "umur": 0,
      "bibit": {
        "id": "bibit1",
        "nama": "Bibit Tomat",
        "photo": "https://example.com/bibit1.jpg",
        "deskripsi": "Bibit tomat unggul",
        "harga_beli": 10000,
        "jenis": "Sayuran",
        "link_market": "https://tani.iyabos.com/marketplace"
      },
      "aktivitas": [
        {
          "id": "aktivitas1",
          "nama": "Pemupukan",
          "keterangan": "Pemupukan tahap 1",
          "pupuk": 1,
          "tanggal_aktifitas": "2023-06-04"
        }
      ]
    }
  }
}