import streamlit as st
import json

# 加載 JSON 檔案
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 單份料理營養計算
def calculate_nutrition(ingredients, portion_sizes):
    nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for ingredient, portion in zip(ingredients, portion_sizes):
        nutrition["calories"] += ingredient["calories"] * portion / 100
        nutrition["protein"] += ingredient["protein"] * portion / 100
        nutrition["fat"] += ingredient["fat"] * portion / 100
        nutrition["carbohydrate"] += ingredient["carbohydrate"] * portion / 100
    return nutrition

# 總營養需求計算
def calculate_total_nutrition_with_gender(base_nutrition, group_population, nutrition_requirements):
    total_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for group, count in group_population.items():
        if group in nutrition_requirements:
            requirements = nutrition_requirements[group]
            for nutrient, value in requirements.items():
                total_nutrition[nutrient] += value * count
    return total_nutrition

# 主程式
def main():
    st.title("午餐營養菜單生成器")
    st.write("根據輸入的人群分佈和食材生成符合營養需求的菜單")

    # 步驟 1：輸入人群分佈
    st.header("步驟 1：輸入人群分佈")
    adults_male = st.number_input("成人男性數量", min_value=0, value=2, step=1)
    adults_female = st.number_input("成人女性數量", min_value=0, value=1, step=1)
    school_male = st.number_input("國小男生數量", min_value=0, value=3, step=1)
    school_female = st.number_input("國小女生數量", min_value=0, value=2, step=1)
    preschool_male = st.number_input("幼兒男孩數量", min_value=0, value=1, step=1)
    preschool_female = st.number_input("幼兒女孩數量", min_value=0, value=1, step=1)
    group_population = {
        "adult_male": adults_male,
        "adult_female": adults_female,
        "school_male": school_male,
        "school_female": school_female,
        "preschool_male": preschool_male,
        "preschool_female": preschool_female,
    }

    # 定義營養需求
    nutrition_requirements = {
        "adult_male": {"calories": 2000, "protein": 60, "fat": 65, "carbohydrate": 300},
        "adult_female": {"calories": 1700, "protein": 50, "fat": 55, "carbohydrate": 255},
        "school_male": {"calories": 1800, "protein": 55, "fat": 60, "carbohydrate": 270},
        "school_female": {"calories": 1600, "protein": 48, "fat": 52, "carbohydrate": 240},
        "preschool_male": {"calories": 1300, "protein": 40, "fat": 45, "carbohydrate": 200},
        "preschool_female": {"calories": 1200, "protein": 36, "fat": 39, "carbohydrate": 180},
    }

    # 定義多道菜的菜品及食材
    st.header("步驟 2：生成多道菜的菜單")
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
    st.subheader("菜單營養內容：")
    for course, details in menu.items():
        nutrition = calculate_nutrition(details["ingredients"], details["portions"])
        st.write(f"{course}：{details['name']} - {nutrition}")
        for key in total_menu_nutrition:
            total_menu_nutrition[key] += nutrition[key]

    # 計算總營養需求
    total_nutrition = calculate_total_nutrition_with_gender(total_menu_nutrition, group_population, nutrition_requirements)
    st.subheader("總營養需求：")
    st.write(total_nutrition)

# 執行主程式
if __name__ == "__main__":
    main()
