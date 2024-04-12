import os
from google.cloud import texttospeech

import io
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret.json'

# テキスト、言語、音声性別を設定しAPIに渡す
def synthesize_speech(text, lang='日本語', gender='male'):
    # 音声性別のタイプ
    gender_type = {
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }
    # 言語
    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }

    # CloudAPIを使用できるようにする
    client = texttospeech.TextToSpeechClient()

    # 音声化するテキストを設定する
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 音声生成の際のパラメータ設定
    # 言語、音声を設定
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    # MP3で書き出す設定
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # 上で設定したパラメータをAPIに渡す
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response

st.title('音声出力アプリ')

st.markdown('### データ準備')

# デフォルトの文字を設定
input_data = st.text_area('こちらにテキストを入力してください。', 'Cloud Speech-to-Text用のサンプル文になります。')

if input_data is not None:
    st.write('入力データ')
    st.write(input_data)
    st.markdown('### パラメータ設定')
    st.subheader('言語と話者の性別選択')

    lang = st.selectbox(
        '言語を選択してください',
        ('日本語', '英語')
    )
    gender = st.selectbox(
        '話者の性別を選択してください',
        ('male', 'female', 'neutral')
    )
    st.markdown('### 音声合成')
    st.write('こちらの文章で音声ファイルの生成を行いますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します')
        response = synthesize_speech(input_data, lang=lang, gender=gender)
        st.audio(response.audio_content)
        comment.write('完了しました')