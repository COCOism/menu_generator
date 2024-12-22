import streamlit as st
import random

# 單份料理營養計算
def calculate_nutrition(ingredients, portion_sizes):
    nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for ingredient, portion in zip(ingredients, portion_sizes):
        nutrition["calories"] += ingredient["calories"] * portion / 100
        nutrition["protein"] += ingredient["protein"] * portion / 100
        nutrition["fat"] += ingredient["fat"] * portion / 100
        nutrition["carbohydrate"] += ingredient["carbohydrate"] * portion / 100
    return nutrition

# 計算中餐營養需求
def calculate_lunch_nutrition(group_population, nutrition_requirements):
    lunch_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for group, count in group_population.items():
        if group in nutrition_requirements:
            requirements = nutrition_requirements[group]
            for nutrient, value in requirements.items():
                lunch_nutrition[nutrient] += value * count * 0.4  # 中餐占 40%
    return lunch_nutrition

# 定義菜單生成邏輯
def generate_menu():
    # 示例菜單池
    menu_pool = {
        "主食": [
            {"name": "米飯", "ingredients": [{"ingredient": "米飯", "calories": 130, "protein": 2.4, "fat": 0.3, "carbohydrate": 28.2}], "portions": [200]},
            {"name": "糙米飯", "ingredients": [{"ingredient": "糙米", "calories": 150, "protein": 3, "fat": 0.5, "carbohydrate": 30}], "portions": [200]},
        ],
        "主菜": [
            {"name": "雞肉炒菜", "ingredients": [{"ingredient": "雞肉", "calories": 165, "protein": 31, "fat": 3.6, "carbohydrate": 0}, {"ingredient": "青椒", "calories": 20, "protein": 0.9, "fat": 0.2, "carbohydrate": 4.6}], "portions": [150, 50]},
            {"name": "紅燒魚", "ingredients": [{"ingredient": "魚肉", "calories": 200, "protein": 25, "fat": 10, "carbohydrate": 1}], "portions": [180]},
        ],
        "副菜": [
            {"name": "胡蘿蔔拌沙拉", "ingredients": [{"ingredient": "胡蘿蔔", "calories": 41, "protein": 0.9, "fat": 0.2, "carbohydrate": 9.6}, {"ingredient": "沙拉醬", "calories": 300, "protein": 1, "fat": 25, "carbohydrate": 12}], "portions": [100, 20]},
            {"name": "炒時蔬", "ingredients": [{"ingredient": "青菜", "calories": 30, "protein": 1.5, "fat": 0.3, "carbohydrate": 5}], "portions": [150]},
        ],
        "湯品": [
            {"name": "紫菜蛋花湯", "ingredients": [{"ingredient": "紫菜", "calories": 10, "protein": 1.7, "fat": 0.1, "carbohydrate": 1.8}, {"ingredient": "雞蛋", "calories": 155, "protein": 13, "fat": 11, "carbohydrate": 1}], "portions": [5, 50]},
            {"name": "冬瓜排骨湯", "ingredients": [{"ingredient": "冬瓜", "calories": 25, "protein": 0.5, "fat": 0.2, "carbohydrate": 5}, {"ingredient": "排骨", "calories": 180, "protein": 15, "fat": 12, "carbohydrate": 0}], "portions": [200, 100]},
        ]
    }
    menu = {course: random.choice(options) for course, options in menu_pool.items()}
    return menu

# 主程式
def main():
    st.title("午餐營養菜單生成器")
    st.write("根據輸入的人群分佈生成符合營養需求的午餐菜單")

    # 定義營養需求
    nutrition_requirements = {
        "adult_male": {"calories": 2000, "protein": 60, "fat": 65, "carbohydrate": 300},
        "adult_female": {"calories": 1700, "protein": 50, "fat": 55, "carbohydrate": 255},
        "school_male": {"calories": 1800, "protein": 55, "fat": 60, "carbohydrate": 270},
        "school_female": {"calories": 1600, "protein": 48, "fat": 52, "carbohydrate": 240},
        "preschool_male": {"calories": 1300, "protein": 40, "fat": 45, "carbohydrate": 200},
        "preschool_female": {"calories": 1200, "protein": 36, "fat": 39, "carbohydrate": 180},
    }

    # 輸入人群分佈
    st.sidebar.header("人群分佈輸入")
    adults_male = st.sidebar.number_input("成人男性數量", min_value=0, value=2, step=1)
    adults_female = st.sidebar.number_input("成人女性數量", min_value=0, value=1, step=1)
    school_male = st.sidebar.number_input("國小男生數量", min_value=0, value=3, step=1)
    school_female = st.sidebar.number_input("國小女生數量", min_value=0, value=2, step=1)
    preschool_male = st.sidebar.number_input("幼兒男孩數量", min_value=0, value=1, step=1)
    preschool_female = st.sidebar.number_input("幼兒女孩數量", min_value=0, value=1, step=1)
    group_population = {
        "adult_male": adults_male,
        "adult_female": adults_female,
        "school_male": school_male,
        "school_female": school_female,
        "preschool_male": preschool_male,
        "preschool_female": preschool_female,
    }

    # 計算中餐營養需求
    lunch_nutrition = calculate_lunch_nutrition(group_population, nutrition_requirements)

    # 菜單生成
    st.header("生成的菜單")
    if st.button("重新生成菜單"):
        menu = generate_menu()
    else:
        menu = generate_menu()

    # 顯示菜單
    for course, details in menu.items():
        st.subheader(f"{course}：{details['name']}")
        st.write("食材分量：")
        for ingredient, portion in zip(details["ingredients"], details["portions"]):
            st.write(f"- {ingredient['ingredient']}: {portion} 克")

    # 顯示營養需求
    st.header("中餐營養需求")
    st.write(lunch_nutrition)

# 執行主程式
if __name__ == "__main__":
    main()
