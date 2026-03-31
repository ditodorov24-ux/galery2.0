import streamlit as st
st.set_page_config(page_title="Галерия животни", layout="wide")
st.title("🐾 Галерия от любими животни")
if "animals" not in st.session_state:
    st.session_state.animals = []

# ======================
# Добавяне на животно
# ======================
st.header("➕ Добави ново животно")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Име")
    species = st.selectbox("Вид", ["Куче", "Котка", "Птица", "Риба", "Друго"])
    age = st.number_input("Възраст", min_value=0, max_value=100, step=1)

with col2:
    description = st.text_area("Описание")
    image_url = st.text_input("URL на картинка")
    rating = st.slider("Рейтинг ⭐", 1, 5, 3)
    favorite = st.checkbox("Любимо ❤️")

if st.button("Добави животно"):
    if name and description and image_url:
        st.session_state.animals.append({
            "име": name,
            "вид": species,
            "възраст": age,
            "описание": description,
            "картинка": image_url,
            "рейтинг": rating,
            "любимо": favorite
        })
        st.success(f"{name} е добавено!")
    else:
        st.warning("Попълнете всички задължителни полета!")

# ======================
# Филтри и търсене
# ======================
st.header("🔍 Търсене и филтри")

search = st.text_input("Търси по име")
filter_species = st.selectbox("Филтър по вид", ["Всички", "Куче", "Котка", "Птица", "Риба", "Друго"])
only_favorites = st.checkbox("Само любими ❤️")

filtered_animals = []

for a in st.session_state.animals:
    if search.lower() not in a["име"].lower():
        continue
    if filter_species != "Всички" and a["вид"] != filter_species:
        continue
    if only_favorites and not a["любимо"]:
        continue
    filtered_animals.append(a)

# ======================
# Премахване
# ======================
st.header("❌ Премахни животно")

if st.session_state.animals:
    names = [a["име"] for a in st.session_state.animals]
    remove_name = st.selectbox("Избери животно", names)

    if st.button("Премахни избраното"):
        st.session_state.animals = [
            a for a in st.session_state.animals if a["име"] != remove_name
        ]
        st.success(f"{remove_name} е премахнато!")
else:
    st.info("Няма животни за премахване.")

# ======================
# Галерия
# ======================
st.header("🖼️ Галерия")

if filtered_animals:
    cols = st.columns(3)

    for idx, animal in enumerate(filtered_animals):
        with cols[idx % 3]:
            st.subheader(animal["име"])

            st.image(animal["картинка"], use_column_width=True)

            st.write(f"**Вид:** {animal['вид']}")
            st.write(f"**Възраст:** {animal['възраст']} години")
            st.write(f"**Рейтинг:** {'⭐' * animal['рейтинг']}")

            if animal["любимо"]:
                st.markdown("❤️ **Любимо**")

            with st.expander("Описание"):
                st.write(animal["описание"])
else:
    st.info("Няма резултати по зададените филтри.")

# ======================
# Статистика
# ======================
st.header("📊 Статистика")

total = len(st.session_state.animals)
favorites = len([a for a in st.session_state.animals if a["любимо"]])

st.write(f"Общо животни: **{total}**")
st.write(f"Любими: **{favorites}**")

if total > 0:
    avg_rating = sum(a["рейтинг"] for a in st.session_state.animals) / total
    st.write(f"Среден рейтинг: **{avg_rating:.2f} ⭐**")
