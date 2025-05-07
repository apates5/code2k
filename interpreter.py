from os.path import dirname, join
import random

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


def main():
    this_folder = dirname(__file__)
    grammar_path = join(this_folder, '2kscript.tx')
    program_path = join(this_folder, 'dabishVsMe.code2k')

    mm = metamodel_from_file(grammar_path, debug=False)

    metamodel_export(mm, join(this_folder, '2kscript_meta.dot'))

    model = mm.model_from_file(program_path)

    model_export(model, join(this_folder, 'contest_model.dot'))

    difficulty_mods = {
        'Rookie': 1.1,
        'Pro': 1.0,
        'AllStar': 0.9,
        'Superstar': 0.85,
        'HallOfFame': 0.75
    }

    form_mods = {
        'Fast': 1.05,
        'Smooth': 1.00,
        'Slow': 0.95
    }

    player_data = {}
    for player in model.players:
        stats = {attr.name: attr.value for attr in player.attributes}
        player_data[player.name] = stats

    for game in model.games:
        shots = game.shots
        difficulty = game.difficulty
        difficulty_modifier = difficulty_mods.get(difficulty, 1.0)
        fizzbuzz_mode = getattr(game, 'fizzbuzz', False)

        print(f"\n3-Point Contest (Difficulty: {difficulty}, Shots: {shots})")
        if fizzbuzz_mode:
            print("Mode: FizzBuzz\n")
        results = []

        for player_ref in game.players:
            name = player_ref.name
            stats = player_data[name]
            three_point = stats.get("rating", 50)
            form = stats.get("form", "Smooth")
            form_modifier = form_mods.get(form, 1.0)
            final_modifier = difficulty_modifier * form_modifier

            made = 0
            for shot_num in range(1, shots + 1):
                is_made = random.random() * 100 <= three_point * final_modifier

                if fizzbuzz_mode:
                    fizzbuzz_tag = ""
                    if shot_num % 3 == 0 and shot_num % 5 == 0:
                        fizzbuzz_tag = "FizzBuzz"
                    elif shot_num % 3 == 0:
                        fizzbuzz_tag = "Fizz"
                    elif shot_num % 5 == 0:
                        fizzbuzz_tag = "Buzz"

                    shot_result = "Made" if is_made else "Missed"

                    if fizzbuzz_tag:
                        print(f"{name} - Shot {shot_num}: {fizzbuzz_tag} ({shot_result})")
                    else:
                        print(f"{name} - Shot {shot_num}: {shot_result}")

                if is_made:
                    made += 1

            print(f"{name} ({form}): {made}/{shots} shots made")
            results.append((name, made))

        max_score = max(score for _, score in results)
        winners = [name for name, score in results if score == max_score]
        print(f"\nWinner(s): {', '.join(winners)}")


if __name__ == "__main__":
    main()