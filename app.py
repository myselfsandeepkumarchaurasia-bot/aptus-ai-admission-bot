import streamlit as st

from database.database import (
    create_tables,
    save_lead
)

from ai.chatbot import (
    create_chatbot,
    generate_response
)

from utils.helpers import build_context
from utils.lead_manager import (
    is_valid_phone,
    is_valid_email
)


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Aptus Academy AI Counsellor",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

create_tables()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7fff7;
}

.chat-header {

    background: linear-gradient(
        90deg,
        #12372A,
        #436850
    );

    padding: 25px;

    border-radius: 15px;

    color: white;

    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="chat-header">

<h1>🎓 Aptus Academy</h1>

<h3>AI Admission Counsellor</h3>

<p>
Learn Skills + Prepare for Jobs + Crack Exams
</p>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📚 Aptus Academy")

    st.write("""
    Our AI Counsellor can help you with:

    • Courses  
    • Fees  
    • Duration  
    • Career Roadmap  
    • Eligibility  
    • Admission  
    • Counselling
    """)

    st.divider()

    st.success(
        "Need personal counselling? "
        "Submit your details."
    )


# --------------------------------------------------
# API
# --------------------------------------------------

if "chatbot" not in st.session_state:

    api_key = st.secrets["GEMINI_API_KEY"]

    st.session_state.chatbot = create_chatbot(
        api_key
    )


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",

            "content":
            """
            👋 Welcome to Aptus Academy!

            I am your AI Admission Counsellor.

            I can help you choose the right course,
            understand fees, duration and career options.

            What would you like to learn?
            """
        }

    ]


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask about courses, fees, career, admission..."
)


if user_input:

    st.session_state.messages.append({

        "role": "user",

        "content": user_input

    })

    with st.chat_message("user"):

        st.write(user_input)


    context = build_context()


    response = generate_response(

        st.session_state.chatbot,

        user_input,

        context

    )


    st.session_state.messages.append({

        "role": "assistant",

        "content": response

    })


    with st.chat_message("assistant"):

        st.write(response)


# --------------------------------------------------
# LEAD FORM
# --------------------------------------------------

st.divider()

st.subheader("📞 Want Personal Career Counselling?")


with st.form("lead_form"):

    name = st.text_input("Full Name")

    phone = st.text_input(
        "Mobile Number"
    )

    email = st.text_input(
        "Email"
    )

    education = st.text_input(
        "Education"
    )

    course = st.selectbox(

        "Interested Course",

        [
            "Data Analytics",
            "Data Science",
            "AI & Machine Learning",
            "Generative AI",
            "Not Sure"
        ]

    )

    career = st.text_input(
        "Career Goal"
    )

    experience = st.selectbox(

        "Experience",

        [
            "Student",
            "Fresher",
            "0-2 Years",
            "2-5 Years",
            "5+ Years"
        ]

    )

    counselling = st.radio(

        "Need Counselling?",

        [
            "Yes",
            "No"
        ]

    )

    submit = st.form_submit_button(
        "🚀 Request Counselling"
    )


    if submit:

        if not name:

            st.error(
                "Please enter your name."
            )

        elif not is_valid_phone(phone):

            st.error(
                "Please enter a valid 10-digit mobile number."
            )

        elif email and not is_valid_email(email):

            st.error(
                "Please enter a valid email."
            )

        else:

            save_lead(

                name,
                phone,
                email,
                education,
                course,
                career,
                experience,
                counselling

            )

            st.success(
                "Thank you! Our admission counsellor "
                "will contact you."
            )