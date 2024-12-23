import streamlit as st
import random

# 食材池（示例）
INGREDIENT_POOL = [
    {"ingredient": "米飯", "type": "vegan", "category": "主食", "calories": 130, "protein": 2.4, "fat": 0.3, "carbohydrate": 28.2},
    {"ingredient": "糙米", "type": "vegan", "category": "主食", "calories": 150, "protein": 3, "fat": 0.5, "carbohydrate": 30},
    {"ingredient": "雞肉", "type": "non_veg", "category": "主菜", "calories": 165, "protein": 31, "fat": 3.6, "carbohydrate": 0},
    {"ingredient": "豬肉", "type": "non_veg", "category": "主菜", "calories": 250, "protein": 30, "fat": 20, "carbohydrate": 0},
    {"ingredient": "牛肉", "type": "non_veg", "category": "主菜", "calories": 250, "protein": 26, "fat": 15, "carbohydrate": 2},
    {"ingredient": "魚肉", "type": "non_veg", "category": "主菜", "calories": 200, "protein": 25, "fat": 10, "carbohydrate": 1},
    {"ingredient": "米粉", "type": "vegan", "category": "主食", "calories": 130, "protein": 2, "fat": 0.5, "carbohydrate": 30},
    {"ingredient": "青椒", "type": "vegan", "category": "蔬菜", "calories": 20, "protein": 0.9, "fat": 0.2, "carbohydrate": 4.6},
    {"ingredient": "胡蘿蔔", "type": "vegan", "category": "蔬菜", "calories": 41, "protein": 0.9, "fat": 0.2, "carbohydrate": 9.6},
]

# 初始化已使用的食材
def init_used_ingredients():
    if "used_ingredients" not in st.session_state:
        st.session_state["used_ingredients"] = set()  # 使用集合避免食材重複

# 避免重複的食材
def filter_available_ingredients(diet_type, category=None):
    available_pool = [
        item for item in INGREDIENT_POOL
        if item["ingredient"] not in st.session_state["used_ingredients"]
    ]
    if diet_type == "普通":
        filtered = available_pool
    elif diet_type == "素食":
        filtered = [item for item in available_pool if item["type"] == "vegan"]
    elif diet_type == "蛋奶素":
        filtered = [item for item in available_pool if item["type"] in ["vegan", "ovo_lacto"]]

    # 筛选指定类别的食材
    if category:
        filtered = [item for item in filtered if item.get("category") == category]
    return filtered

# 隨機生成主菜（限定米飯、面或米粉類）
def generate_main_dish(diet_type):
    main_dish_pool = filter_available_ingredients(diet_type, category="主食")
    if not main_dish_pool:
        return {"name": "主菜 - 無可用食材", "ingredients": [], "portions": []}

    selected_ingredient = random.choice(main_dish_pool)
    st.session_state["used_ingredients"].add(selected_ingredient["ingredient"])
    return {
        "name": f"主菜 - {selected_ingredient['ingredient']}",
        "ingredients": [selected_ingredient],
        "portions": [random.randint(150, 250)],
    }

# 隨機生成其他菜品
def generate_random_dish(course_name, diet_type, category=None):
    available_pool = filter_available_ingredients(diet_type, category)
    if not available_pool:
        return {"name": f"{course_name} - 無可用食材", "ingredients": [], "portions": []}

    num_ingredients = min(len(available_pool), random.randint(1, 3))  # 避免超出可用食材數量
    selected_ingredients = random.sample(available_pool, num_ingredients)
    for ingredient in selected_ingredients:
        st.session_state["used_ingredients"].add(ingredient["ingredient"])
    portion_sizes = [random.randint(50, 150) for _ in selected_ingredients]  # 每種食材隨機分配 50-150 克
    return {
        "name": f"{course_name} - 隨機料理",
        "ingredients": selected_ingredients,
        "portions": portion_sizes,
    }

# 初始化人群分布數據
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

# 初始化菜單
def init_menu():
    if "menu" not in st.session_state:
        st.session_state["menu"] = {
            "主食": generate_main_dish("普通"),
            "主菜": generate_main_dish("普通"),
            "副菜": generate_random_dish("副菜", "普通", category="蔬菜"),
            "湯品": generate_random_dish("湯品", "普通"),
        }

# 主程式
def main():
    st.title("午餐營養菜單生成器")

    # 初始化狀態
    init_population_data()
    init_used_ingredients()
    init_menu()

    # 左侧栏：人群分布输入
    with st.sidebar:
        st.header("人群分布輸入")
        st.session_state["population_data"]["adult_male"] = st.number_input("成人男性數量", min_value=0, value=2, step=1)
        st.session_state["population_data"]["adult_female"] = st.number_input("成人女性數量", min_value=0, value=1, step=1)
        st.session_state["population_data"]["school_male"] = st.number_input("國小男生數量", min_value=0, value=3, step=1)
        st.session_state["population_data"]["school_female"] = st.number_input("國小女生數量", min_value=0, value=2, step=1)
        st.session_state["population_data"]["preschool_male"] = st.number_input("幼兒男孩數量", min_value=0, value=1, step=1)
        st.session_state["population_data"]["preschool_female"] = st.number_input("幼兒女孩數量", min_value=0, value=1, step=1)

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
            st.button(f"重新生成 {course}", key=f"regenerate_{course}")

# 執行主程式
if __name__ == "__main__":
    main()
