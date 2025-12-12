import uuid
import streamlit as st
from llm import stream_ai_message


st.set_page_config(page_title='전세사기피해 상담 챗봇', page_icon='🍀')
st.title('🍀 전세사기피해 상담 챗봇')


st.markdown("""
    <style>
    /* 모든 st.button 공통 스타일 (지금은 FAQ 버튼만 있음) */
    div.stButton > button {
        width: 100%;
        text-align: left;             /* 텍스트 왼쪽 정렬 */
        justify-content: flex-start;  /* 버튼 안에서 내용 왼쪽으로 */
        background-color: #f8f8f8;    /* 기본 배경: 아주 연한 회색 */
        color: #333333;               /* 글자색: 진한 회색 */
        border: 1px solid #e0e0e0;    /* 테두리: 연한 회색 */
        border-radius: 999px;         /* pill 형태 둥근 모서리 (선택) */
    }

    /* 마우스 올렸을 때 */
    div.stButton > button:hover {
        background-color: #eeeeee;    /* 살짝 더 진한 회색 */
        color: #222222;
        border-color: #d0d0d0;
    }

    /* 클릭/선택(active, focus) 상태일 때도 빨간색 안 나오도록 */
    div.stButton > button:focus, 
    div.stButton > button:active {
        background-color: #eeeeee;
        color: #222222;
        border-color: #d0d0d0;
        box-shadow: none;
    }
    </style>
""", unsafe_allow_html=True)

# print('\n\n== start ==')
# print('before) st.session_state >>', st.session_state)

## ================================================================================
## URL의 parameter에 session id 가져오기/저장 
## ================================================================================
query_params = st.query_params

if 'session_id' in query_params:
    session_id = query_params['session_id']
else :
    session_id = str(uuid.uuid4())
    st.query_params.update({'session_id': session_id})

## Streamlit 내부 세션: session id 저장 
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = session_id

## Streamlit 내부 세션: 메시지 리스트 초기화
if 'message_list' not in st.session_state:
    st.session_state.message_list = []

# print('after) st.session_state >>', st.session_state)


## ================================================================================
## FAQ 버튼 섹션 
## ================================================================================
st.markdown('### 자주 묻는 질문(FAQ)')

SUGGESTED_QUESTIONS = [
    '전세사기를 당했습니다. 어떤 법적 조치를 해야 하나요?',
    '전세사기 피해 신고 절차는 어떻게 되나요?',
    '전세사기 피해 보상을 받을 수 있는 방법이 있나요?',
    '전세사기피해자입니다. 전세사기피해자 기준을 알려주세요.'
]

for i, question in enumerate(SUGGESTED_QUESTIONS):
    if st.button(question, use_container_width=True, key=f'suggested_{i}'):
        ## 사용자 질문
        st.session_state.message_list.append({'role': 'user', 'content': question})

        ## AI 답변 생성
        with st.spinner('답변 생성하는 중입니다.'):
            session_id = st.session_state.session_id
            ai_message = stream_ai_message(question, session_id=session_id)

            ## Streamlit 화면 출력
            ai_message = st.write_stream(ai_message)

        ## 메시지 히스토리에 추가
        st.session_state.message_list.append({'role': 'ai', 'content': ai_message})

        ## 화면 새로고침
        st.rerun()

st.divider()


## ================================================================================
## 이전 채팅 내용 화면 출력 
## ================================================================================
for message in st.session_state.message_list:
    with st.chat_message(message['role']):
        st.write(message['content'])


## ================================================================================
## 사용자 질문 -> AI 답변 생성
## ================================================================================
placeholder = '전세사기피해와 관련된 궁금한 내용을 질문하세요.'

if user_question := st.chat_input(placeholder=placeholder): ## prompt 창
    ## 사용자 메시지 ##############################
    with st.chat_message('user'):
        ## 사용자 메시지 화면 출력
        st.write(user_question)
    st.session_state.message_list.append({'role': 'user', 'content': user_question})

    ## AI 메시지 ##################################
    with st.spinner('답변 생성하는 중입니다.'):
        session_id = st.session_state.session_id
        ai_message = stream_ai_message(user_question, session_id=session_id)

        with st.chat_message('ai'):
            ## AI 메시지 화면 출력
            ai_message = st.write_stream(ai_message)
        st.session_state.message_list.append({'role': 'ai', 'content': ai_message})
