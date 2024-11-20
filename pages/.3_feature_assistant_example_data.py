import streamlit as st
import test_chat

st.header('Example data for feature extraction')

st.write("""
Paste this content into the Document Content field to test the feature
extraction function.
""".strip())

st.code(test_chat.context, language=None)

st.write("""Consider defining some of the following features""")

st.markdown("""
| Name | Type | Enum Values| Description |
|------|------|------------|-------------|
| label | string | | letter of the alphabet identifying the biopsy |
| gleason_score | string | | The gleason score of the prostate cancer |
| location | string | | Anatomic location of the biopsy within the prostate |
| diagnosis | string | benign, malignant | Histological diagnosis of the biopsy |
| biopsy_length | number | | Length of the entore biopsy core in cm |
| cancer_length | number | | Length of the cancer within the biopsy core in cm|
""")
