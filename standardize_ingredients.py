def standardize_ingredients(data):
    standardized_data = []
    for item in data:
        standardized_item = {}

        # 保留 ingredient 欄位
        standardized_item["ingredient"] = item.get("ingredient", "").strip()

        # 處理 aliases 欄位：兼容字符串、列表和空值
        aliases = item.get("aliases", "")
        if isinstance(aliases, str):
            # 如果是字符串，按逗號分隔為列表
            standardized_item["aliases"] = [alias.strip() for alias in aliases.split(",") if alias.strip()]
        elif isinstance(aliases, list):
            # 如果是數組，保留原樣
            standardized_item["aliases"] = aliases
        else:
            # 如果為其他類型（如 None），設置為空列表
            standardized_item["aliases"] = []

        # 將營養數據移至 nutrition_per_100g
        nutrition = {}
        for key, value in item.items():
            if "Calories" in key:
                nutrition["calories"] = value
            elif "Protein" in key:
                nutrition["protein"] = value
            elif "Fat" in key:
                nutrition["fat"] = value
            elif "Carbohydrate" in key:
                nutrition["carbohydrate"] = value

        standardized_item["nutrition_per_100g"] = nutrition
        standardized_data.append(standardized_item)

    return standardized_data
