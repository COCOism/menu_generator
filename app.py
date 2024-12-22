import streamlit as st

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

    # 定義營養需求
    nutrition_requirements = {
        "adult_male": {"calories": 2000, "protein": 60, "fat": 65, "carbohydrate": 300},
        "adult_female": {"calories": 1700, "protein": 50, "fat": 55, "carbohydrate": 255},
        "school_male": {"calories": 1800, "protein": 55, "fat": 60, "carbohydrate": 270},
        "school_female": {"calories": 1600, "protein": 48, "fat": 52, "carbohydrate": 240},
        "preschool_male": {"calories": 1300, "protein": 40, "fat": 45, "carbohydrate": 200},
        "preschool_female": {"calories": 1200, "protein": 36, "fat": 39, "carbohydrate": 180},
    }

    # 使用列布局
    col1, col2 = st.columns(2)

    # 左側顯示總營養需求
    with col1:
        st.header("總營養需求")
        total_menu_nutrition = {"calories": 1500, "protein": 75, "fat": 50, "carbohydrate": 200}  # 示例菜單營養
        st.write("菜單總營養：", total_menu_nutrition)

    # 右側顯示人群分佈輸入
    with col2:
        st.header("人群分佈輸入")
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

    # 計算總營養需求
    total_nutrition = calculate_total_nutrition_with_gender(
        total_menu_nutrition, group_population, nutrition_requirements
    )
    with col1:
        st.subheader("人群需求總營養：")
        st.write(total_nutrition)

# 執行主程式
if __name__ == "__main__":
    main()
