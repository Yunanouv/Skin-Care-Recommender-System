import streamlit as st
from streamlit_option_menu import option_menu
from numpy.core.fromnumeric import prod
import tensorflow as tf
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

# Import the Dataset 
skincare = pd.read_csv("skincare.csv", encoding='utf-8', index_col=None)

# Header
st.set_page_config(page_title="Aplikasi Rekomendasi Produk Skin Care", page_icon=":blossom:", layout="wide",)

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 2


def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Skin Care", "Get Recommendation", "Skin Care 101"],  # required
                icons=["house", "stars", "book"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Skin Care", "Get Recommendation", "Skin Care 101"],  # required
            icons=["house", "stars", "book"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Skin Care", "Get Recommendation", "Skin Care 101"],  # required
            icons=["house", "stars", "book"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected


selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "Skin Care":
    st.title(f"Aplikasi Rekomendasi Produk {selected} :sparkles:")
    st.write('---') 

    st.write(
        """
        ##### **Aplikasi Rekomendasi Produk Skin Care merupakan salah satu implementasi Machine Learning yang dapat memberikan rekomendasi produk skin care sesuai dengan jenis dan juga permasalahan kulit Anda**
        """)
    
    #displaying a local video file

    video_file = open("skincare.mp4", "rb").read()
    st.video(video_file, start_time = 1) #displaying the video 
    
    st.write(' ') 
    st.write(' ')
    st.write(
        """
        ##### Anda akan mendapatkan rekomendasi produk skin care dari berbagai macam brand kosmetik dengan total 1200+ produk yang disesuaikan dengan kebutuhan kulit Anda. 
        ##### Terdapat 5 kategori produk skin care dengan 5 tipe kulit berbeda, serta permasalahan dan manfaat yang ingin didapatkan dari produk. Aplikasi rekomendasi ini hanyalah sebuah sistem yang memberikan rekomendasi sesuai dengan data yang Anda masukkan. 
        """)
    
    st.write(
        """
        **Silahkan pilih halaman *Get Recommendation* untuk mulai mendapatkan rekomendasi Atau pilih halaman *Skin Care 101* untuk melihat tips dan trik seputar skin care**
        """)
    
    st.write(
        """
        **Selamat Mencoba :) !**
        """)
    
    
    st.info('Credit: Created by Dwi Ayu Nouvalina')

if selected == "Get Recommendation":
    st.title(f"Let's {selected}")
    
    st.write(
        """
        ##### **Untuk mendapatkan rekomendasi, silahkan masukkan jenis kulit, keluhan, dan manfaat yang diinginkan untuk mendapatkan rekomendasi produk skin care yang tepat**
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
    def skincare_recommendations(nama_produk, similarity_data=cosine_sim_df, items=skincare[['product_name', 'description']], k=5):

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
    
    
if selected == "Skin Care 101":
    st.title(f"Take a Look at {selected}")
    st.write('---') 

    st.write(
        """
        ##### **Berikut adalah tips dan trik yang bisa Anda ikuti untuk memaksimalkan penggunaan produk skin care**
        """) 
    
    image = Image.open('imagepic.jpg')
    st.image(image, caption='Skin Care 101')
    

    
    st.write(
        """
        ### **1. Facial Wash**
        """)
    st.write(
        """
        **- Gunakanlah produk facial wash yang telah direkomendasikan atau yang sudah cocok untuk Anda**
        """)
    st.write(
        """
        **- Cuci muka maksimal 2 kali sehari yaitu di pagi hari dan malam sebelum tidur. Mencuci wajah terlalu sering akan menghilangkan minyak alami kulit. Bagi Anda pemilik wajah kering, tidak masalah jika di pagi hari hanya menggunakan air biasa**
        """)
    st.write(
        """
        **- Jangan menggosok wajah dengan kasar karena dapat menghilangkan pelindung alami kulit**
        """)
    st.write(
        """
        **- Cara terbaik untuk membersihkan kulit adalah menggunakan ujung jari antara 30-60 detik dengan gerakan memutar dan memijat**
        """)
    
    st.write(
        """
        ### **2. Toner**
        """)
    st.write(
        """
        **- Gunakanlah toner yang telah direkomendasikan atau yang sudah cocok untuk Anda**
        """)
    st.write(
        """
        **- Tuangkan toner ke kapas lalu usap lembut ke wajah. Untuk hasil yang lebih maksimal, gunakanlah 2 layer toner dimana yang pertama menggunakan kapas dan yang terakhir menggunakan tangan agar lebih meresap**
        """)
    st.write(
        """
        **- Gunakan toner sehabis mencuci wajah**
        """)
    st.write(
        """
        **- Bagi Anda pemilik kulit sensitif, sebisa mungkin hindarilah produk skin care yang mengandung fragrance**
        """)
    
    st.write(
        """
        ### **3. Serum**
        """)
    st.write(
        """
        **- Gunakanlah serum yang telah direkomendasikan atau yang sudah cocok untuk Anda untuk hasil lebih maksimal**
        """)
    st.write(
        """
        **- Serum digunakan setelah wajah benar-benar bersih agar kandungan serum menyerap sempurna**
        """)
    st.write(
        """
        **- Gunakan serum di pagi dan malam hari sebelum tidur**
        """)
    st.write(
        """
        **- Pilihlah serum sesuai dengan kebutuhan Anda seperti menghilangkan bekas jerawat atau menghilangkan flek hitam atau anti-aging ataupun manfaat lainnya**
        """)
    st.write(
        """
        **- Cara memakai serum agar menyerap lebih sempurna adalah tuangkan ke telapak tangan lalu tepuk perlahan-lahan ke wajah dan tunggu hingga meresap**
        """)
    
    st.write(
        """
        ### **4. Moisturizer**
        """)
    st.write(
        """
        **- Gunakanlah moisturizer (pelembap) yang telah direkomendasikan atau yang sudah cocok untuk Anda untuk hasil lebih maksimal**
        """)
    st.write(
        """
        **- Moisturizer adalah produk skin care wajib yang harus dimiliki karena mampu mengunci kelembapan dan berbagai nutrisi dari serum yang telah digunakan**
        """)
    st.write(
        """
        **- Untuk hasil lebih maksimal, gunakanlah pelembap yang berbeda di pagi dan malam hari. Pelembap pagi biasanya dilengkapi dengan sunscreen dan vitamin untuk melindungi kulit dari efek buruk sinar UV dan polusi, sementara pelembap malam mengandung berbagai bahan aktif yang membantu proses regenerasi kulit saat tidur**
        """)
    st.write(
        """
        **- Berilah jeda waktu antara penggunaan serum dan pelembap sekitar 2-3 menit untuk memastikan serum sudah meresap ke dalam kulit**
        """)
    
    st.write(
        """
        ### **5. Sunscreen**
        """)
    st.write(
        """
        **- Gunakanlah sunscreen (tabir surya) yang telah direkomendasikan atau yang sudah cocok untuk Anda untuk hasil lebih maksimal**
        """)
    st.write(
        """
        **- Sunscreen adalah kunci utama semua produk skin care karena melindungi kulit dari efek bahaya sinar UVA dan UVB, bahkan light blue. Semua produk skin care akan tidak terasa manfaatnya jika tidak ada yang melindungi kulit**
        """)
    st.write(
        """
        **- Gunakanlah sunscreen kurang lebih sepanjang jari telunjuk dan tengah tangan untuk memaksimalkan perlindungan**
        """)
    st.write(
        """
        **- Re-apply sunscreen setiap 2-3 jam sekali atau sebanyak yang dibutuhkan**
        """)
    st.write(
        """
        **- Tetap menggunakan sunscreen meskipun di dalam rumah karena sinar matahari di jam 10 ke atas tetap tembus melewati jendela dan pada saat cuaca mendung**
        """)
    
    st.write(
        """
        ### **6. Jangan gonta-ganti skin care**
        """)
    st.write(
        """
        **Sering gonta-ganti skin care akan menyababkan kulit wajah mengalami stress karena harus beradaptasi dengan kandungan produk. Alhasil manfaat yang didapat tidak 100%. Sebaliknya, gunakanlah produk skin care selama berbulan-bulan untuk melihat hasilnya**
        """)
    
    st.write(
        """
        ### **7. Konsisten**
        """)
    st.write(
        """
        **Kunci dari perawatan wajah adalah konsistensi. Rajin dan tekunlah dalam menggunakan produk skin care karena hasil yang didapat tidak bersifat instan**
        """)
    st.write(
        """
        ### **8. Wajah adalah aset**
        """)
    st.write(
        """
        **Berbagai rupa manusia adalah karunia yang diberikan oleh sang Pencipta. Rawatlah karunia itu dengan baik dan sungguh-sungguh sebagai bentuk rasa syukur. Pilihlah produk dan cara perawatan yang sesuai dengan kebutuhan kulit. Menggunakan produk skin care sejak dini sama saja dengan investasi di masa tua.**
        """)
     
    
    
