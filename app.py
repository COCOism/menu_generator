import streamlit as st
import random

# 食材池
INGREDIENT_POOL = [
    {"ingredient": "米飯", "type": "vegan", "category": "主食", "calories": 130, "protein": 2.4, "fat": 0.3, "carbohydrate": 28.2},
    {"ingredient": "糙米", "type": "vegan", "category": "主食", "calories": 150, "protein": 3, "fat": 0.5, "carbohydrate": 30},
    {"ingredient": "米粉", "type": "vegan", "category": "主食", "calories": 130, "protein": 2, "fat": 0.5, "carbohydrate": 30},
    {"ingredient": "雞肉", "type": "non_veg", "category": "雞", "calories": 165, "protein": 31, "fat": 3.6, "carbohydrate": 0},
    {"ingredient": "豬肉", "type": "non_veg", "category": "豬", "calories": 250, "protein": 30, "fat": 20, "carbohydrate": 0},
    {"ingredient": "牛肉", "type": "non_veg", "category": "牛", "calories": 250, "protein": 26, "fat": 15, "carbohydrate": 2},
    {"ingredient": "魚肉", "type": "non_veg", "category": "魚", "calories": 200, "protein": 25, "fat": 10, "carbohydrate": 1},
    {"ingredient": "青椒", "type": "vegan", "category": "蔬菜", "calories": 20, "protein": 0.9, "fat": 0.2, "carbohydrate": 4.6},
    {"ingredient": "胡蘿蔔", "type": "vegan", "category": "蔬菜", "calories": 41, "protein": 0.9, "fat": 0.2, "carbohydrate": 9.6},
]

# 初始化已使用的食材
def init_used_ingredients():
    if "used_ingredients" not in st.session_state:
        st.session_state["used_ingredients"] = set()

# 避免食材重复
def filter_available_ingredients(category=None):
    available_pool = [item for item in INGREDIENT_POOL if item["ingredient"] not in st.session_state["used_ingredients"]]
    if category:
        return [item for item in available_pool if item.get("category") == category]
    return available_pool

# 动态根据人数调整食材总量
def calculate_total_portion(base_portion):
    population = sum(st.session_state["population_data"].values())
    return int(base_portion * population / 10)  # 假设 10 人为基准

# 生成主菜
def generate_main_dish(category):
    meat_pool = filter_available_ingredients(category)
    if not meat_pool:
        return {"name": "主菜 - 無可用食材", "ingredients": [], "portions": []}

    meat = random.choice(meat_pool)
    st.session_state["used_ingredients"].add(meat["ingredient"])
    return {
        "name": f"主菜 - {meat['ingredient']}",
        "ingredients": [meat],
        "portions": [calculate_total_portion(200)],
    }

# 生成主食（米饭、面或米粉）
def generate_main_food():
    main_food_pool = filter_available_ingredients("主食")
    if not main_food_pool:
        return {"name": "主食 - 無可用食材", "ingredients": [], "portions": []}

    selected_food = random.choice(main_food_pool)
    st.session_state["used_ingredients"].add(selected_food["ingredient"])
    return {
        "name": f"主食 - {selected_food['ingredient']}",
        "ingredients": [selected_food],
        "portions": [calculate_total_portion(150)],
    }

# 生成其他菜品
def generate_random_dish(course_name, category=None):
    available_pool = filter_available_ingredients(category)
    if not available_pool:
        return {"name": f"{course_name} - 無可用食材", "ingredients": [], "portions": []}

    num_ingredients = min(len(available_pool), random.randint(1, 3))
    selected_ingredients = random.sample(available_pool, num_ingredients)
    for ingredient in selected_ingredients:
        st.session_state["used_ingredients"].add(ingredient["ingredient"])
    portions = [calculate_total_portion(50) for _ in selected_ingredients]
    return {
        "name": f"{course_name} - 隨機料理",
        "ingredients": selected_ingredients,
        "portions": portions,
    }

# 初始化人群分布
def init_population_data():
    if "population_data" not in st.session_state:
        st.session_state["population_data"] = {
            "adult_male": 2,
            "adult_female": 1,
            "school_male": 3,
            "school_female": 2,
            "preschool_male": 1,
            "preschool_female": 1,
        }

# 初始化菜单
def init_menu():
    if "menu" not in st.session_state:
        st.session_state["menu"] = {
            "主食": generate_main_food(),
            "主菜": generate_main_dish("雞"),
            "副菜": generate_random_dish("副菜", "蔬菜"),
            "湯品": generate_random_dish("湯品"),
        }

# 主程式
def main():
    st.title("午餐營養菜單生成器")

    # 初始化状态
    init_population_data()
    init_used_ingredients()
    init_menu()

    # 左侧栏：人群分布
    with st.sidebar:
        st.header("人群分布輸入")
        for group in st.session_state["population_data"]:
            st.session_state["population_data"][group] = st.number_input(
                f"{group} 數量", min_value=0, value=st.session_state["population_data"][group], step=1
            )

    # 主页面内容
    st.header("生成的菜單")
    for course in ["主食", "主菜", "副菜", "湯品"]:
        col1, col2 = st.columns([3, 1])
        with col1:
            details = st.session_state["menu"][course]
            st.subheader(f"{course}：{details['name']}")
            st.write("食材分量：")
            for ingredient, portion in zip(details["ingredients"], details["portions"]):
                st.write(f"- {ingredient['ingredient']}: {portion} 克")

        with col2:
            if course == "主菜":
                st.selectbox(
                    "選擇主菜類型",
                    ["雞", "豬", "牛", "魚"],
                    key="main_dish_category",
                    on_change=lambda: st.session_state["menu"].update({"主菜": generate_main_dish(st.session_state["main_dish_category"])}),
                )
            st.button(f"重新生成 {course}", key=f"regenerate_{course}", on_click=lambda c=course: regenerate_course(c))

# 重新生成某道菜
def regenerate_course(course):
    if course == "主食":
        st.session_state["menu"]["主食"] = generate_main_food()
    elif course == "主菜":
        st.session_state["menu"]["主菜"] = generate_main_dish(st.session_state["main_dish_category"])
    elif course == "副菜":
        st.session_state["menu"]["副菜"] = generate_random_dish("副菜", "蔬菜")
    elif course == "湯品":
        st.session_state["menu"]["湯品"] = generate_random_dish("湯品")

if __name__ == "__main__":
    main()
