import streamlit as st
import matplotlib.pyplot as plt

# 單份料理營養計算
def calculate_nutrition(ingredients, portion_sizes):
    nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for ingredient, portion in zip(ingredients, portion_sizes):
        nutrition["calories"] += ingredient["calories"] * portion / 100
        nutrition["protein"] += ingredient["protein"] * portion / 100
        nutrition["fat"] += ingredient["fat"] * portion / 100
        nutrition["carbohydrate"] += ingredient["carbohydrate"] * portion / 100
    return nutrition

# 主程式
def main():
    st.title("午餐營養菜單生成器")
    st.write("根據輸入的人群分佈和食材生成符合營養需求的菜單")

    # 定義多道菜的菜品及食材
    menu = {
        "主食": {
            "name": "米飯",
            "ingredients": [{"ingredient": "米飯", "calories": 130, "protein": 2.4, "fat": 0.3, "carbohydrate": 28.2}],
            "portions": [200]  # 米飯200克
        },
        "主菜": {
            "name": "雞肉炒菜",
            "ingredients": [
                {"ingredient": "雞肉", "calories": 165, "protein": 31, "fat": 3.6, "carbohydrate": 0},
                {"ingredient": "青椒", "calories": 20, "protein": 0.9, "fat": 0.2, "carbohydrate": 4.6}
            ],
            "portions": [150, 50]  # 雞肉150克，青椒50克
        },
        "副菜": {
            "name": "胡蘿蔔拌沙拉",
            "ingredients": [
                {"ingredient": "胡蘿蔔", "calories": 41, "protein": 0.9, "fat": 0.2, "carbohydrate": 9.6},
                {"ingredient": "沙拉醬", "calories": 300, "protein": 1, "fat": 25, "carbohydrate": 12}
            ],
            "portions": [100, 20]  # 胡蘿蔔100克，沙拉醬20克
        },
        "湯品": {
            "name": "紫菜蛋花湯",
            "ingredients": [
                {"ingredient": "紫菜", "calories": 10, "protein": 1.7, "fat": 0.1, "carbohydrate": 1.8},
                {"ingredient": "雞蛋", "calories": 155, "protein": 13, "fat": 11, "carbohydrate": 1}
            ],
            "portions": [5, 50]  # 紫菜5克，雞蛋50克
        }
    }

    # 計算每道菜的營養
    total_menu_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    st.header("菜單詳細內容")
    for course, details in menu.items():
        nutrition = calculate_nutrition(details["ingredients"], details["portions"])
        st.subheader(f"{course}：{details['name']}")
        st.write("食材分量：")
        for ingredient, portion in zip(details["ingredients"], details["portions"]):
            st.write(f"- {ingredient['ingredient']}: {portion} 克")
        st.write("營養內容：", nutrition)
        for key in total_menu_nutrition:
            total_menu_nutrition[key] += nutrition[key]

    # 將英文轉為中文
    nutrition_labels = {
        "calories": "熱量 (卡路里)",
        "protein": "蛋白質 (克)",
        "fat": "脂肪 (克)",
        "carbohydrate": "碳水化合物 (克)"
    }
    nutrition_data = {nutrition_labels[key]: value for key, value in total_menu_nutrition.items()}

    # 營養數據展示
    st.subheader("菜單總營養內容")
    for label, value in nutrition_data.items():
        st.write(f"{label}：{value}")

    # 繪製圖表
    st.subheader("菜單營養內容圖表")
    fig, ax = plt.subplots()
    ax.bar(nutrition_data.keys(), nutrition_data.values(), color='skyblue')
    ax.set_ylabel("含量")
    ax.set_title("菜單營養內容")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 執行主程式
if __name__ == "__main__":
    main()
