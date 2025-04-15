import streamlit as st
import json
import os

# 📂 JSON File Setup
LIBRARY_FILE = "library.json"

# 📌 Function: Load Library Data
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# 📌 Function: Save Library Data
def save_library(books):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(books, file, indent=4)

# 📌 Load Data
library = load_library()

# 🎨 Soft Gradient Background
page_bg_gradient = '''
<style>
/* Soft Gradient Background */
.stApp {
    background: linear-gradient(to right, #dde5f4, #cfd9e9); /* Light Blue to Soft Purple */
    color: black;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #2c3e50, #bdc3c7); /* Muted Dark Blue to Light Grey */
    color: white;
}

/* Text Customization */
h1, h2, h3, h4, h5, h6, p, label {
    color: black !important;
}
</style>
'''
st.markdown(page_bg_gradient, unsafe_allow_html=True)

# 🏛️ Library Manager UI
st.title("📚 Personal Library Manager")
st.sidebar.title("📖 Library Menu")

# 📌 Menu Options
menu = ["Add Book", "Remove Book", "Search Book", "Display Books", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

# 🛠️ Add Book Feature
if choice == "Add Book":
    st.subheader("📝 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")

    if st.button("📖 Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }
        library.append(new_book)
        save_library(library)
        st.success(f'✅ "{title}" by {author} added to your library!')

# ❌ Remove Book
elif choice == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    if library:
        book_titles = [book["title"] for book in library]
        book_to_remove = st.selectbox("Select a book to remove", book_titles)

        if st.button("🗑️ Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f'❌ "{book_to_remove}" removed from your library!')
    else:
        st.warning("No books available to remove!")

# 🔍 Search Book
elif choice == "Search Book":
    st.subheader("🔎 Search for a Book")
    search_option = st.radio("Search by", ["Title", "Author"])
    search_query = st.text_input(f"Enter {search_option}")

    if st.button("🔍 Search"):
        results = []
        if search_option == "Title":
            results = [book for book in library if search_query.lower() in book["title"].lower()]
        elif search_option == "Author":
            results = [book for book in library if search_query.lower() in book["author"].lower()]

        if results:
            for idx, book in enumerate(results, start=1):
                st.write(f"📖 **{idx}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

# 📚 Display Books
elif choice == "Display Books":
    st.subheader("📚 Your Library Collection")
    if library:
        for idx, book in enumerate(library, start=1):
            st.write(f"📖 **{idx}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("No books in the library yet!")

# 📊 Statistics
elif choice == "Statistics":
    st.subheader("📊 Library Stats")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books}")
    st.write(f"📊 **Read Percentage:** {percentage_read:.2f}%")

# 🚀 Footer
st.sidebar.markdown("---")
st.sidebar.write("👩‍💻 Developed By Muskan Irfan Ahmed")
