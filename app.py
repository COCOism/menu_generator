import streamlit as st
import random

# 食材池（示例）
INGREDIENT_POOL = [
    {"ingredient": "米飯", "type": "vegan", "calories": 130, "protein": 2.4, "fat": 0.3, "carbohydrate": 28.2},
    {"ingredient": "糙米", "type": "vegan", "calories": 150, "protein": 3, "fat": 0.5, "carbohydrate": 30},
    {"ingredient": "雞肉", "type": "non_veg", "category": "雞", "calories": 165, "protein": 31, "fat": 3.6, "carbohydrate": 0},
    {"ingredient": "豬肉", "type": "non_veg", "category": "豬", "calories": 250, "protein": 30, "fat": 20, "carbohydrate": 0},
    {"ingredient": "牛肉", "type": "non_veg", "category": "牛", "calories": 250, "protein": 26, "fat": 15, "carbohydrate": 2},
    {"ingredient": "魚肉", "type": "non_veg", "category": "魚", "calories": 200, "protein": 25, "fat": 10, "carbohydrate": 1},
    {"ingredient": "青椒", "type": "vegan", "calories": 20, "protein": 0.9, "fat": 0.2, "carbohydrate": 4.6},
    {"ingredient": "胡蘿蔔", "type": "vegan", "calories": 41, "protein": 0.9, "fat": 0.2, "carbohydrate": 9.6},
    {"ingredient": "沙拉醬", "type": "ovo_lacto", "calories": 300, "protein": 1, "fat": 25, "carbohydrate": 12},
    {"ingredient": "紫菜", "type": "vegan", "calories": 10, "protein": 1.7, "fat": 0.1, "carbohydrate": 1.8},
    {"ingredient": "雞蛋", "type": "ovo_lacto", "calories": 155, "protein": 13, "fat": 11, "carbohydrate": 1},
]

# 篩選可用食材
def filter_available_ingredients(diet_type, exclude_categories=None):
    available_pool = INGREDIENT_POOL
    if diet_type == "普通":
        filtered = available_pool
    elif diet_type == "素食":
        filtered = [item for item in available_pool if item["type"] == "vegan"]
    elif diet_type == "蛋奶素":
        filtered = [item for item in available_pool if item["type"] in ["vegan", "ovo_lacto"]]

    # 排除特定類別的食材
    if exclude_categories:
        filtered = [item for item in filtered if item.get("category") not in exclude_categories]
    return filtered

# 隨機生成其他菜品
def generate_random_dish(course_name, diet_type):
    available_pool = filter_available_ingredients(diet_type)
    if not available_pool:
        return {"name": f"{course_name} - 無可用食材", "ingredients": [], "portions": []}

    num_ingredients = min(len(available_pool), random.randint(2, 4))  # 避免超出可用食材數量
    selected_ingredients = random.sample(available_pool, num_ingredients)
    portion_sizes = [random.randint(50, 200) for _ in selected_ingredients]  # 每種食材隨機分配 50-200 克
    return {
        "name": f"{course_name} - 隨機料理",
        "ingredients": selected_ingredients,
        "portions": portion_sizes,
    }

# 隨機生成主菜
def generate_main_dish(diet_type, category):
    meat_pool = [item for item in INGREDIENT_POOL if item.get("category") == category]
    if not meat_pool:
        return {"name": "主菜 - 無可用食材", "ingredients": [], "portions": []}

    meat = random.choice(meat_pool)  # 強制選擇一種肉類
    non_meat_pool = filter_available_ingredients(diet_type, exclude_categories=[category])
    num_ingredients = min(len(non_meat_pool), random.randint(1, 3))  # 1-3 種搭配食材
    other_ingredients = random.sample(non_meat_pool, num_ingredients)
    selected_ingredients = [meat] + other_ingredients
    portion_sizes = [random.randint(100, 200) if item == meat else random.randint(50, 150) for item in selected_ingredients]
    return {
        "name": f"主菜 - {meat['ingredient']} 搭配",
        "ingredients": selected_ingredients,
        "portions": portion_sizes,
    }

# 初始化菜單類型
def init_diet_types():
    if "diet_types" not in st.session_state:
        st.session_state["diet_types"] = {
            "主食": "普通",
            "主菜": "普通",
            "副菜": "普通",
            "湯品": "普通",
        }

# 初始化主菜選擇類別
def init_main_dish_category():
    if "main_dish_category" not in st.session_state:
        st.session_state["main_dish_category"] = "雞"  # 默認為雞

# 初始化菜單
def init_menu():
    if "menu" not in st.session_state:
        st.session_state["menu"] = {
            "主食": generate_random_dish("主食", st.session_state["diet_types"]["主食"]),
            "主菜": generate_main_dish(st.session_state["diet_types"]["主菜"], st.session_state["main_dish_category"]),
            "副菜": generate_random_dish("副菜", st.session_state["diet_types"]["副菜"]),
            "湯品": generate_random_dish("湯品", st.session_state["diet_types"]["湯品"]),
        }

# 主程式
def main():
    st.title("午餐營養菜單生成器")

    # 初始化狀態
    init_diet_types()
    init_main_dish_category()
    init_menu()

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
                    on_change=lambda: regenerate_main_dish(),
                )
            st.button(f"重新生成 {course}", key=f"regenerate_{course}")

# 回调函数生成主菜
def regenerate_main_dish():
    st.session_state["menu"]["主菜"] = generate_main_dish(
        st.session_state["diet_types"]["主菜"], st.session_state["main_dish_category"]
    )

# 執行主程式
if __name__ == "__main__":
    main()
