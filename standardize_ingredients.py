import json

# 加载 JSON 文件
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 保存 JSON 文件
def save_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 标准化食材数据
def standardize_ingredients(data):
    standardized_data = []
    for item in data:
        try:
            standardized_item = {}

            # 处理 ingredient 字段
            standardized_item["ingredient"] = item.get("ingredient", "").strip()

            # 处理 aliases 字段
            aliases = item.get("aliases", "")
            if isinstance(aliases, str):
                # 如果是字符串，按逗号分隔为列表
                standardized_item["aliases"] = [alias.strip() for alias in aliases.split(",") if alias.strip()]
            elif isinstance(aliases, list):
                # 如果是列表，直接保留
                standardized_item["aliases"] = aliases
            else:
                # 如果为其他类型或缺失，设置为空列表
                standardized_item["aliases"] = []

            # 处理营养字段
            nutrition = {
                "calories": item.get("Calories (per 100g)", 0.0),
                "protein": item.get("Protein (per 100g)", 0.0),
                "fat": item.get("Fat (per 100g)", 0.0),
                "carbohydrate": item.get("Carbohydrate (per 100g)", 0.0)
            }
            standardized_item["nutrition_per_100g"] = nutrition

            # 添加处理后的数据
            standardized_data.append(standardized_item)

        except Exception as e:
            print(f"处理数据失败：{item}，错误信息：{e}")

    return standardized_data

# 主程序
def main():
    input_file = "ingredients.json"  # 原始数据文件路径
    output_file = "standardized_ingredients.json"  # 标准化后文件路径

    # 加载数据
    raw_data = load_data(input_file)

    # 标准化数据
    standardized_data = standardize_ingredients(raw_data)

    # 保存标准化数据
    save_data(standardized_data, output_file)
    print(f"标准化完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
