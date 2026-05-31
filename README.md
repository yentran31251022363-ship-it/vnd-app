# VietCash · Nhận Diện Tiền Việt Nam

Web app nhận diện 11 mệnh giá tiền VN bằng CNN (MobileNetV2 Transfer Learning).

## Cấu trúc project

```
tienVN/
├── app.py                  ← Streamlit app
├── requirements.txt        ← Dependencies
├── .streamlit/
│   └── config.toml         ← Theme dark/gold
└── model/
    └── tienVN_*.keras      ← Đặt file model vào đây  ← QUAN TRỌNG
```

## Deploy lên Streamlit Cloud (miễn phí)

### Bước 1 — Chuẩn bị model
1. Chạy notebook `CNN_TienVietNam_Drive.ipynb` trên Colab
2. Download file `.keras` về máy
3. Đặt vào thư mục `model/` trong project này

### Bước 2 — Push lên GitHub
```bash
git init
git add .
git commit -m "VietCash CNN app"
git remote add origin https://github.com/<username>/vietcash.git
git push -u origin main
```

> ⚠️ File model `.keras` thường > 100MB → dùng **Git LFS**:
> ```bash
> git lfs install
> git lfs track "*.keras" "*.h5"
> git add .gitattributes
> git add model/
> ```

### Bước 3 — Deploy Streamlit Cloud
1. Vào [share.streamlit.io](https://share.streamlit.io)
2. **New app** → chọn repo GitHub
3. Main file: `app.py`
4. Deploy → xong!

## Chạy local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset
[Nguyễn Trọng Đại – Vietnamese Currency (Kaggle)](https://www.kaggle.com/datasets/nguyentrongdai/vietnamese-currency)
