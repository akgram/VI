import pygame
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen settings
WIDTH, HEIGHT = 600, 400
FONT_SIZE = 24

# Initialize Pygame
pygame.init()
font = pygame.font.Font(None, FONT_SIZE)

def show_message(screen, message):
    """Displays a message box on the screen."""
    message_box = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 4)
    pygame.draw.rect(screen, WHITE, message_box)
    pygame.draw.rect(screen, BLACK, message_box, 2)

    # Display the message
    message_surface = font.render(message, True, RED)
    ok_button = pygame.Rect(message_box.x + message_box.width // 2 - 50, message_box.y + message_box.height - 40, 100, 30)
    pygame.draw.rect(screen, GRAY, ok_button)
    ok_text = font.render("OK", True, BLACK)

    # Center the message
    screen.blit(
        message_surface,
        (message_box.x + (message_box.width - message_surface.get_width()) // 2, message_box.y + 20)
    )
    screen.blit(
        ok_text,
        (ok_button.x + (ok_button.width - ok_text.get_width()) // 2, ok_button.y + 5)
    )
    pygame.display.flip()

    # Wait for user to close the message box
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and ok_button.collidepoint(event.pos):
                waiting = False

def draw_grid(screen, dimension):
    """Draws a grid of the specified dimension."""
    screen.fill(WHITE)
    cell_size = min(WIDTH, HEIGHT) // dimension

    for row in range(dimension):
        for col in range(dimension):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.display.flip()

def game_screen(dimension):
    """Game screen that shows the grid."""
    game_running = True
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tabla")

    draw_grid(game_screen, dimension)

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

    pygame.quit()
    sys.exit()

def main_screen():
    """Main screen for inputting data."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Unos Podataka")
    
    input_boxes = [
        {"label": "Ko igra prvi? (covek/racunar):", "value": "", "rect": pygame.Rect(50, 50, 400, 30), "active": False},
        {"label": "Simbol prvog igraca (X/O):", "value": "", "rect": pygame.Rect(50, 120, 400, 30), "active": False},
        {"label": "Dimenzija table (4-8):", "value": "", "rect": pygame.Rect(50, 190, 400, 30), "active": False}
    ]
    button_rect = pygame.Rect(200, 270, 200, 50)
    active_box = None

    running = True
    while running:
        screen.fill(WHITE)

        # Draw input fields and labels
        for box in input_boxes:
            label_surface = font.render(box["label"], True, BLACK)
            screen.blit(label_surface, (box["rect"].x, box["rect"].y - 30))

            pygame.draw.rect(screen, BLUE if box["active"] else GRAY, box["rect"], 2)
            text_surface = font.render(box["value"], True, BLACK)
            screen.blit(text_surface, (box["rect"].x + 5, box["rect"].y + 5))

        # Draw button
        pygame.draw.rect(screen, GRAY, button_rect)
        button_text = font.render("Start", True, BLACK)
        screen.blit(button_text, (button_rect.x + 60, button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse click to activate a box
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in input_boxes:
                    if box["rect"].collidepoint(event.pos):
                        box["active"] = True
                        active_box = box
                    else:
                        box["active"] = False

                # Check if button is clicked
                if button_rect.collidepoint(event.pos):
                    first = input_boxes[0]["value"].lower()
                    simbol = input_boxes[1]["value"].upper()
                    dimension = input_boxes[2]["value"]

                    if first not in ["covek", "racunar"]:
                        show_message(screen, "Greška: Prvi igrač mora biti 'covek' ili 'racunar'!")
                    elif simbol not in ["X", "O"]:
                        show_message(screen, "Greška: Simbol mora biti 'X' ili 'O'!")
                    elif not dimension.isdigit() or int(dimension) not in range(4, 9):
                        show_message(screen, "Greška: Dimenzija mora biti broj između 4 i 8!")
                    else:
                        running = False
                        game_screen(int(dimension))

            # Handle typing in the active input box
            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_RETURN:
                    active_box["active"] = False
                    active_box = None
                elif event.key == pygame.K_BACKSPACE:
                    active_box["value"] = active_box["value"][:-1]
                else:
                    active_box["value"] += event.unicode

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_screen()
