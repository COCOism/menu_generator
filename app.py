import streamlit as st
import random

# 食材池（示例）
INGREDIENT_POOL = [
    {"ingredient": "米飯", "calories": 130, "protein": 2.4, "fat": 0.3, "carbohydrate": 28.2},
    {"ingredient": "糙米", "calories": 150, "protein": 3, "fat": 0.5, "carbohydrate": 30},
    {"ingredient": "雞肉", "calories": 165, "protein": 31, "fat": 3.6, "carbohydrate": 0},
    {"ingredient": "青椒", "calories": 20, "protein": 0.9, "fat": 0.2, "carbohydrate": 4.6},
    {"ingredient": "胡蘿蔔", "calories": 41, "protein": 0.9, "fat": 0.2, "carbohydrate": 9.6},
    {"ingredient": "沙拉醬", "calories": 300, "protein": 1, "fat": 25, "carbohydrate": 12},
    {"ingredient": "紫菜", "calories": 10, "protein": 1.7, "fat": 0.1, "carbohydrate": 1.8},
    {"ingredient": "雞蛋", "calories": 155, "protein": 13, "fat": 11, "carbohydrate": 1},
    {"ingredient": "牛肉", "calories": 250, "protein": 26, "fat": 15, "carbohydrate": 2},
    {"ingredient": "魚肉", "calories": 200, "protein": 25, "fat": 10, "carbohydrate": 1},
]

# 單份料理營養計算
def calculate_nutrition(ingredients, portion_sizes):
    nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for ingredient, portion in zip(ingredients, portion_sizes):
        nutrition["calories"] += ingredient["calories"] * portion / 100
        nutrition["protein"] += ingredient["protein"] * portion / 100
        nutrition["fat"] += ingredient["fat"] * portion / 100
        nutrition["carbohydrate"] += ingredient["carbohydrate"] * portion / 100
    return nutrition

# 隨機生成菜品
def generate_random_dish(course_name):
    num_ingredients = random.randint(2, 4)  # 每道菜隨機包含 2-4 種食材
    selected_ingredients = random.sample(INGREDIENT_POOL, num_ingredients)
    portion_sizes = [random.randint(50, 200) for _ in selected_ingredients]  # 每種食材隨機分配 50-200 克
    dish_name = f"{course_name} - 隨機料理"
    return {
        "name": dish_name,
        "ingredients": selected_ingredients,
        "portions": portion_sizes,
    }

# 計算中餐營養需求
def calculate_lunch_nutrition(group_population, nutrition_requirements):
    lunch_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for group, count in group_population.items():
        if group in nutrition_requirements:
            requirements = nutrition_requirements[group]
            for nutrient, value in requirements.items():
                lunch_nutrition[nutrient] += value * count * 0.4  # 中餐占 40%
    return lunch_nutrition

# 主程式
def main():
    st.title("午餐營養菜單生成器")
    st.write("根據動態生成的隨機食材組合生成午餐菜單，並計算中餐營養需求")

    # 人群輸入（側欄）
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

    # 定義人群營養需求
    nutrition_requirements = {
        "adult_male": {"calories": 2000, "protein": 60, "fat": 65, "carbohydrate": 300},
        "adult_female": {"calories": 1700, "protein": 50, "fat": 55, "carbohydrate": 255},
        "school_male": {"calories": 1800, "protein": 55, "fat": 60, "carbohydrate": 270},
        "school_female": {"calories": 1600, "protein": 48, "fat": 52, "carbohydrate": 240},
        "preschool_male": {"calories": 1300, "protein": 40, "fat": 45, "carbohydrate": 200},
        "preschool_female": {"calories": 1200, "protein": 36, "fat": 39, "carbohydrate": 180},
    }

    # 計算中餐營養需求
    lunch_nutrition = calculate_lunch_nutrition(group_population, nutrition_requirements)
    st.sidebar.subheader("中餐營養需求")
    st.sidebar.write(lunch_nutrition)

    # 初始化菜單
    if "menu" not in st.session_state:
        st.session_state["menu"] = {
            "主食": generate_random_dish("主食"),
            "主菜": generate_random_dish("主菜"),
            "副菜": generate_random_dish("副菜"),
            "湯品": generate_random_dish("湯品"),
        }

    # 顯示菜單並提供重新生成按鈕
    st.header("生成的菜單")
    for course in ["主食", "主菜", "副菜", "湯品"]:
        col1, col2 = st.columns([3, 1])
        with col1:
            details = st.session_state["menu"][course]
            st.subheader(f"{course}：{details['name']}")
            st.write("食材分量：")
            for ingredient, portion in zip(details["ingredients"], details["portions"]):
                st.write(f"- {ingredient['ingredient']}: {portion} 克")

            # 計算總營養
            nutrition = calculate_nutrition(details["ingredients"], details["portions"])
            st.write("總營養素：", nutrition)

        with col2:
            if st.button(f"重新生成 {course}", key=course):
                st.session_state["menu"][course] = generate_random_dish(course)
                st.experimental_rerun()

# 執行主程式
if __name__ == "__main__":
    main()
