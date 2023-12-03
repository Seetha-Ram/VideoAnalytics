import streamlit as st
import webbrowser

def main():
    st.title("Streamlit App")

    if st.button("Pose Estimation"):
        # Replace 'https://your_pose_estimation_link' with the actual link
        open_external_link('https://bumchikk.onrender.com/')

    if st.button("Video Similarity"):
        # Replace 'https://your_video_similarity_link' with the actual link
        open_external_link('https://videosimmilarity.onrender.com/')

def open_external_link(link):
    new_tab = 2  # Open link in a new tab
    webbrowser.open(link, new_tab)

if __name__ == "__main__":
    main()
