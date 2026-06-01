import streamlit as st
import re

# --- 1. 定義データの分離 ---
REQUIREMENTS = {
    "宛名": r".*(さま|様|殿|御中|先生)",
    "挨拶": r"(いつもお世話になっております|お疲れ様です|拝啓|謹啓|お世話になっております|お世話になります|はじめまして)",
    "名乗り": r"(私は|私|沼津高専.*の.*です|.*と申します|MIRS26.*です)",
    "要旨": r"(件名|目的は|について|ご連絡申し上げます|ご連絡いたしました|ご相談です|先日.*件)",
    "詳細": r"(以下の通り|詳細は|下記ご参照ください|【.*】|・|^\d\.)",
    "結びの挨拶": r"(よろしくお願いいたします|よろしくお願い申し上げます|何卒よろしくお願い申し上げます|宜しくお願いします|よろしくお願いします|よろしくお願い致します|よろしくお願いたします)",
    "署名": r"(----------|沼津高専|住所|電話番号|連絡先|沼津工業高等専門学校)"
}

# 不足時のガイド情報
GUIDANCE = {
    "宛名": "宛名はメールの最初に記載します。例：株式会社〇〇 営業部 佐藤様",
    "挨拶": "挨拶から書き始めましょう。例：いつもお世話になっております。",
    "名乗り": "所属と氏名を名乗りましょう。例：沼津高専の山田太郎です。",
    "要旨": "メールの目的を一言で伝えます。例：件名：〇〇の件についてご連絡申し上げます。",
    "詳細": "具体的な内容を箇条書きなどで整理しましょう。例：・日時：6月5日 14:00～",
    "結びの挨拶": "最後にお礼を述べましょう。例：何卒よろしくお願い申し上げます。",
    "署名": "末尾に連絡先を記載します。例：----------\n沼津高専 〇〇学科 山田太郎"
}

# 敬語のチェックリスト
KEIGO_RULES = {
    "ご苦労様です": "お疲れ様です",
    "了解しました": "承知いたしました",
    "拝見させていただきました": "拝見いたしました",
    "お伺いさせていただきます": "伺います",
    "～の方": "～（「の方」は不要な場合が多いです）"
}

# --- 2. UIの構築 ---
st.set_page_config(page_title="ビジネスメールチェッカー", layout="wide")
st.title("✉️ ビジネスメールチェッカー")
st.write("メール本文を入力すると、構成要素と敬語を自動チェックします。")

col1, col2 = st.columns([1, 1])

with col1:
    text = st.text_area("メール本文を入力", height=400)

with col2:
    if st.button("チェックする"):
        if not text.strip():
            st.error("本文を入力してください。")
        else:
            # --- 構成チェック ---
            st.subheader("✅ 構成要素チェック")
            missing_items = []
            
            # 各要素の判定
            for name, pattern in REQUIREMENTS.items():
                if name == "名乗り":
                    # 名乗りは冒頭150文字で判定
                    if not re.search(pattern, text[:150]):
                        missing_items.append(name)
                else:
                    if not re.search(pattern, text):
                        missing_items.append(name)
            
            if not missing_items:
                st.success("構成は完璧です！")
            else:
                st.warning("以下の要素が不足している可能性があります：")
                for item in missing_items:
                    with st.expander(f"📌 {item} のガイド"):
                        st.write(GUIDANCE[item])

            # --- 敬語チェック ---
            st.subheader("⚠️ 敬語・表現チェック")
            found_errors = []
            for ng_word, advice in KEIGO_RULES.items():
                if ng_word in text:
                    found_errors.append((ng_word, advice))
            
            if not found_errors:
                st.success("気になる敬語は見当たりません。")
            else:
                for ng, advice in found_errors:
                    st.error(f"「{ng}」が使われています。 → 「{advice}」への書き換えを推奨します。")
