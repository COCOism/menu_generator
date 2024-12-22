import json
import streamlit as st

# 加載 JSON 數據
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# 計算總午餐需求
def calculate_lunch_nutrition(distribution, requirements):
    total_lunch_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    for group, count in distribution.items():
        lunch_requirements = requirements[group]["lunch"]
        for nutrient, value in lunch_requirements.items():
            total_lunch_nutrition[nutrient] += value * count
    return total_lunch_nutrition

# 根據人數調整食材與營養數據
def adjust_recipe_for_servings(recipe, servings):
    adjusted_ingredients = {key: value * servings for key, value in recipe["ingredients"].items()}
    adjusted_nutrition = {key: value * servings for key, value in recipe.get("nutrition", {}).items()}
    
    adjusted_recipe = recipe.copy()
    adjusted_recipe["ingredients"] = adjusted_ingredients
    adjusted_recipe["nutrition"] = adjusted_nutrition
    
    return adjusted_recipe

# 篩選適合的菜單
def generate_menu(total_nutrition, recipes):
    menu = []
    current_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}
    
    for recipe in recipes:
        can_add = True
        for key in total_nutrition:
            if current_nutrition[key] + recipe["nutrition"][key] > total_nutrition[key]:
                can_add = False
                break
        
        if can_add:
            menu.append(recipe)
            for key in current_nutrition:
                current_nutrition[key] += recipe["nutrition"][key]
                
        if all(current_nutrition[key] >= total_nutrition[key] for key in total_nutrition):
            break

    return menu, current_nutrition

# 主應用程式
def main():
    st.title("午餐營養菜單生成器")
    st.write("根據不同對象分布和營養需求，生成符合條件的午餐菜單")

    # 加載數據
    nutrition_requirements = load_data("nutrition_requirements.json")
    recipes = load_data("recipes.json")
    ingredients = load_data("ingredients.json")
    
    # 使用者輸入對象分布
    st.sidebar.header("輸入對象分布")
    distribution = {
        "adult": st.sidebar.number_input("成人數量", min_value=0, value=2, step=1),
        "primary_school": st.sidebar.number_input("國小學童數量", min_value=0, value=3, step=1),
        "kindergarten": st.sidebar.number_input("幼兒園學童數量", min_value=0, value=1, step=1)
    }

    # 計算午餐總需求
    total_nutrition = calculate_lunch_nutrition(distribution, nutrition_requirements)
    st.subheader("總午餐營養需求")
    st.write(total_nutrition)
    
    # 生成菜單
    menu, achieved_nutrition = generate_menu(total_nutrition, recipes)
    
    st.subheader("生成的菜單")
    if menu:
        for recipe in menu:
            servings = st.sidebar.number_input(f"{recipe['recipe_name']} 的份數", min_value=1, value=1, step=1)
            adjusted_recipe = adjust_recipe_for_servings(recipe, servings)
            
            st.write(f"### {recipe['recipe_name']}（{servings} 人份）")
            st.write("食材需求：")
            for ingredient, amount in adjusted_recipe["ingredients"].items():
                st.write(f"- {ingredient}: {amount} 克")
            st.write("營養數據：")
            for key, value in adjusted_recipe["nutrition"].items():
                st.write(f"- {key}: {value:.2f}")
    else:
        st.warning("無法生成符合條件的菜單，請檢查數據或調整條件。")
    
    st.subheader("實際達成的營養")
    st.write(achieved_nutrition)

if __name__ == "__main__":
    main()