def standardize_ingredients(data):
    standardized_data = []
    for item in data:
        try:
            standardized_item = {}

            # 处理 ingredient 字段
            standardized_item["ingredient"] = item.get("ingredient", "").strip()

            # 处理 aliases 字段：兼容字符串、列表、空值和其他类型
            aliases = item.get("aliases", "")
            if isinstance(aliases, str):
                # 如果是字符串，按逗号分隔为列表
                standardized_item["aliases"] = [alias.strip() for alias in aliases.split(",") if alias.strip()]
            elif isinstance(aliases, list):
                # 如果是列表，直接保留
                standardized_item["aliases"] = aliases
            else:
                # 如果为其他类型或为空值，设置为空列表
                standardized_item["aliases"] = []

            # 处理营养字段，若字段缺失则填充默认值 0.0
            nutrition = {
                "calories": item.get("Calories (per 100g)", 0.0),
                "protein": item.get("Protein (per 100g)", 0.0),
                "fat": item.get("Fat (per 100g)", 0.0),
                "carbohydrate": item.get("Carbohydrate (per 100g)", 0.0)
            }
            standardized_item["nutrition_per_100g"] = nutrition

            # 将处理后的数据加入列表
            standardized_data.append(standardized_item)

        except Exception as e:
            # 捕获异常并打印问题数据
            print(f"数据处理失败：{item}，错误信息：{e}")

    return standardized_data
