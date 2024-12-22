import json

# 加載 JSON 文件
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# 保存 JSON 文件
def save_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 根據食材數據計算每道菜的營養數據
def calculate_recipe_nutrition(recipe, ingredients_data):
    # 初始化營養數據
    nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0}

    # 遍歷每個食材
    for ingredient_name, amount in recipe["ingredients"].items():
        # 找到對應的食材數據
        ingredient_data = next((item for item in ingredients_data if item["ingredient"] == ingredient_name), None)
        if ingredient_data:
            for key in nutrition:
                # 按用量比例計算營養值
                nutrition[key] += (ingredient_data["nutrition_per_100g"][key] * amount / 100)
        else:
            print(f"警告：食材 '{ingredient_name}' 的營養數據缺失，已跳過。")
    
    return nutrition

# 主程式：自動計算所有菜單的營養數據
def main():
    # 加載數據
    ingredients_data = load_data("ingredients.json")
    recipes_data = load_data("recipes.json")

    # 更新每道菜的營養數據
    for recipe in recipes_data:
        # 如果菜單沒有營養數據，則計算並添加
        if "nutrition" not in recipe or not recipe["nutrition"]:
            recipe["nutrition"] = calculate_recipe_nutrition(recipe, ingredients_data)

    # 保存更新後的菜單數據
    save_data(recipes_data, "recipes_with_nutrition.json")
    print("所有菜單的營養數據已計算並保存到 'recipes_with_nutrition.json' 文件中。")

if __name__ == "__main__":
    main()
