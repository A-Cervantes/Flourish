class Question:
    def __init__(self, question_text, choices, correct_choice_index, points=1):
        self.question_text = question_text
        self.choices = choices  # List of strings
        self.correct_choice_index = correct_choice_index  # Index of correct answer
        self.points = points

    def check_answer(self, user_choice):
        return user_choice == self.correct_choice_index + 1
    
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return lines

    def render(self, font, surface, start_y=120, max_width=550, spacing=10, selected_choice=None):
        question_lines = self.wrap_text(self.question_text, font, max_width)
        y = start_y
        for line in question_lines:
            rendered_line = font.render(line, True, (255, 255, 255))
            surface.blit(rendered_line, (120, y))
            y += rendered_line.get_height() + spacing

        # Render choices
        for i, choice in enumerate(self.choices):
            color = (255, 255, 0) if selected_choice == i else (255, 255, 255)
            rendered_choice = font.render(f"{i + 1}. {choice}", True, color)
            surface.blit(rendered_choice, (140, y))
            y += rendered_choice.get_height() + spacing
        

# Level 1 questions
level1_questions = [
    Question(
        "What does a plant need most to perform photosynthesis?",
        ["Sunlight", "Wind", "Rocks", "Sugar"],
        0
    ),
    Question(
        "Which part of the plant absorbs water?",
        ["Leaf", "Root", "Stem", "Flower"],
        1
    ),
    Question(
        "What gas do plants take in for photosynthesis?",
        ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
        1
    ),
]

# Level 2 questions
level2_questions = [
    Question(
        "Which nutrient is essential for strong root growth?",
        ["Nitrogen", "Phosphorus", "Potassium", "Calcium"],
        1
    ),
    Question(
        "What is the process called when water vapor leaves the plant?",
        ["Transpiration", "Respiration", "Photosynthesis", "Condensation"],
        0
    ),
    Question(
        "Which part of the plant makes seeds?",
        ["Root", "Stem", "Leaf", "Flower"],
        3
    ),
]

# Level 3 questions
level3_questions = [
    Question(
        "What pigment gives plants their green color?",
        ["Chlorophyll", "Carotene", "Anthocyanin", "Melanin"],
        0
    ),
    Question(
        "Which of these is NOT a type of pollination?",
        ["Wind", "Water", "Animal", "Fire"],
        3
    ),
    Question(
        "What is the main function of plant stomata?",
        ["Absorb sunlight", "Exchange gases", "Anchor plant", "Store food"],
        1
    ),
]