"""Run all three API demos: python main.py  (needs internet)"""

from src.fruit import fetch_fruit_data, fruits_to_df, get_calories, get_family_and_genus
from src.jokes import fetch_jokes, jokes_to_df
from src.users import get_squad


def run_section(title: str, action) -> None:
    """Run one demo. If its API fails, report it and keep going."""
    print(f"\n=== {title} ===")
    try:
        action()
    except Exception as error:  # network or API errors differ per library
        print(f"Skipped: could not complete this step ({error})")


def demo_squad() -> None:
    squad = get_squad(10)
    print(squad[["Name", "Gender", "City", "Email"]])
    squad.to_csv("output/squad.csv", index=False)
    print("Saved output/squad.csv")


def demo_fruit() -> None:
    fruits = fruits_to_df(fetch_fruit_data())
    print("Fruits loaded:", len(fruits), "| columns:", len(fruits.columns))
    print("Cherry family/genus:", get_family_and_genus(fruits, "Cherry"))
    print("Banana calories:", get_calories(fruits, "Banana"))


def demo_jokes() -> None:
    print(jokes_to_df(fetch_jokes()).head(5).to_string(index=False))


if __name__ == "__main__":
    run_section("1) RandomUser API: placeholder squad", demo_squad)
    run_section("2) Fruityvice API: diet nutrition", demo_fruit)
    run_section("3) Official Joke API: dressing room jokes", demo_jokes)
