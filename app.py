# 主菜生成：指定一种肉类及搭配其他食材
def generate_main_dish(selected_category):
    # 获取符合条件的肉类食材
    meat_pool = [item for item in INGREDIENT_POOL if item["category"] == selected_category and item["ingredient"] not in st.session_state["used_ingredients"]]
    # 获取非肉类的搭配食材
    non_meat_pool = [item for item in INGREDIENT_POOL if item["category"] != selected_category and item["ingredient"] not in st.session_state["used_ingredients"]]

    if not meat_pool:
        return {"name": "主菜 - 無可用肉類", "ingredients": [], "portions": []}

    # 随机选择一种肉品
    meat = random.choice(meat_pool)
    st.session_state["used_ingredients"].add(meat["ingredient"])

    # 随机选择其他非肉类食材作为搭配
    num_non_meat = min(len(non_meat_pool), random.randint(1, 3))
    selected_non_meat = random.sample(non_meat_pool, num_non_meat)

    # 组合肉类和非肉类食材
    ingredients = [meat] + selected_non_meat
    portions = [calculate_total_portion(200) if item == meat else calculate_total_portion(50) for item in ingredients]

    for ingredient in selected_non_meat:
        st.session_state["used_ingredients"].add(ingredient["ingredient"])

    return {"name": f"主菜 - {meat['ingredient']} 搭配", "ingredients": ingredients, "portions": portions}
