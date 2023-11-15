from numpy.core.fromnumeric import prod
import tensorflow as tf
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Import the Dataset 
skincare = pd.read_csv("skincare.csv", encoding='utf-8', index_col=None)

# Header
st.set_page_config(page_title="Aplikasi Rekomendasi Produk Skin Care", page_icon=":blossom:", layout="wide",)

# menampilkan halaman utama
st.title("Aplikasi Rekomendasi Produk Skin Care :sparkles:")

st.write('---') 

#displaying a local video file

video_file = open("skincare.mp4", "rb").read()
st.video(video_file, start_time = 1) #displaying the video 


st.write('---') 

st.write(
    """
    ##### **Aplikasi Rekomendasi Produk Skin Care merupakan sebuah implementasi dari proyek Machine Learning yang dapat memberikan rekomendasi produk skin care sesuai dengan jenis dan juga permasalahan kulit Anda. Anda dapat memasukkan jenis kulit, keluhan, dan manfaat yang diinginkan untuk mendapatkan rekomendasi produk skin care yang tepat**
    """)  
st.write('---') 

first,last = st.columns(2)

# Choose a product product type category
# pt = product type
category = first.selectbox(label='Kategori Produk : ', options= skincare['tipe_produk'].unique() )
category_pt = skincare[skincare['tipe_produk'] == category]

# Choose a skintype
# st = skin type
skin_type = last.selectbox(label='Tipe Kulit Kamu : ', options= ['Normal', 'Dry', 'Oily', 'Combination', 'Sensitive'] )
category_st_pt = category_pt[category_pt[skin_type] == 1]

# pilih keluhan
prob = st.multiselect(label='Permasalahan Kulit Kamu : ', options= ['Kulit Kusam', 'Jerawat', 'Bekas Jerawat','Pori-pori Besar', 'Flek Hitam', 'Garis Halus dan Kerutan', 'Komedo', 'Warna Kulit Tidak Merata', 'Kemerahan', 'Kulit Kendur'] )

# Choose notable_effects
# dari produk yg sudah di filter berdasarkan product type dan skin type(category_st_pt), kita akan ambil nilai yang unik di kolom notable_effects
opsi_ne = category_st_pt['notable_effects'].unique().tolist()
# notable_effects-notable_effects yang unik maka dimasukkan ke dalam variabel opsi_ne dan digunakan untuk value dalam multiselect yg dibungkus variabel selected_options di bawah ini
selected_options = st.multiselect('Manfaat yang Diinginkan : ',opsi_ne)
# hasil dari selected_options kita masukan ke dalam var category_ne_st_pt
category_ne_st_pt = category_st_pt[category_st_pt["notable_effects"].isin(selected_options)]

# Choose product
# produk2 yang sudah di filter dan ada di var filtered_df kemudian kita saring dan ambil yang unik2 saja berdasarkan product_name dan di masukkan ke var opsi_pn
opsi_pn = category_ne_st_pt['product_name'].unique().tolist()
# buat sebuah selectbox yang berisi pilihan produk yg sudah di filter di atas
product = st.selectbox(label='Produk yang Direkomendasikan Untuk Kamu', options = sorted(opsi_pn))
# variabel product di atas akan menampung sebuah produk yang akan memunculkan rekomendasi produk lain

## MODELLING with Content Based Filtering
# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

# Melakukan perhitungan idf pada data 'notable_effects'
tf.fit(skincare['notable_effects']) 

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names()

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(skincare['notable_effects']) 

# Melihat ukuran matrix tfidf
shape = tfidf_matrix.shape

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

# Membuat dataframe untuk melihat tf-idf matrix
# Kolom diisi dengan efek-efek yang diinginkan
# Baris diisi dengan nama produk
pd.DataFrame(
    tfidf_matrix.todense(), 
    columns=tf.get_feature_names(),
    index=skincare.product_name
).sample(shape[1], axis=1).sample(10, axis=0)

# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix) 

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama produk
cosine_sim_df = pd.DataFrame(cosine_sim, index=skincare['product_name'], columns=skincare['product_name'])

# Melihat similarity matrix pada setiap nama produk
cosine_sim_df.sample(7, axis=1).sample(10, axis=0)

# Membuat fungsi untuk mendapatkan rekomendasi
def skincare_recommendations(nama_produk, similarity_data=cosine_sim_df, items=skincare[['product_name', 'produk-href','price', 'description']], k=5):
    
    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan    
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,nama_produk].to_numpy().argpartition(range(-1, -k, -1))
    
    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
    # Drop nama_produk agar nama produk yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(nama_produk, errors='ignore')
    df = pd.DataFrame(closest).merge(items).head(k)
    return df

# Membuat button untuk menampilkan rekomendasi
model_run = st.button('Temukan Rekomendasi Produk Lainnya!')
# Mendapatkan rekomendasi
if model_run:
    st.write('Berikut Rekomendasi Produk Serupa Lainnya Sesuai yang Kamu Inginkan')
    st.write(skincare_recommendations(product))
    st.snow()
